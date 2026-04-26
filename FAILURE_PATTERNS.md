# Drass 项目 Failure Patterns 分析报告

> 分析日期：2026-04-26  
> 扫描范围：全项目源码、配置文件、启动脚本、Docker 编排

---

## 严重程度分布

| 级别 | 数量 | 说明 |
|------|------|------|
| 🔴 CRITICAL | 3 | 可导致服务整体崩溃或数据泄露 |
| 🟠 HIGH | 6 | 可导致功能大范围失效或性能雪崩 |
| 🟡 MEDIUM | 8 | 可导致局部故障或难以排查的隐患 |
| 🔵 LOW | 4 | 代码质量问题，潜在长期风险 |

---

## FP-01 同步阻塞 HTTP 调用（无超时）

**级别：** 🔴 CRITICAL  
**文件：** `services/main-app/app/chains/compliance_rag_chain.py:226-230`

```python
class CustomEmbeddings(Embeddings):
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        response = requests.post(           # ← 同步 requests，无 timeout
            f"{settings.EMBEDDING_API_BASE}/embeddings",
            json={"texts": texts}
        )
        return response.json()["embeddings"]
```

**触发条件：** Embedding Service 响应缓慢、挂起，或网络波动。  
**潜在后果：**
- `requests.post` 默认永久阻塞，会挂死 FastAPI 的 worker 线程池
- 在异步上下文中调用同步 HTTP，会阻塞整个事件循环
- 无重试机制，一次超时即抛异常，导致整条 RAG 链路失败
- 线程池耗尽后，所有新请求 503

**修复方向：** 替换为 `httpx.AsyncClient` 并设置 `timeout=30`，配合 `tenacity` 重试。

---

## FP-02 健康检查无超时保护（雪崩触发器）

**级别：** 🔴 CRITICAL  
**文件：** `services/main-app/app/main.py:166-199`

```python
@app.get("/health")
async def health_check():
    # 无 asyncio.wait_for 包裹，下游超时会拖死此接口
    health_status["services"]["vector_store"] = await vector_store_service.health_check()
    health_status["services"]["llm"]          = await unified_llm_service.health_check()
    health_status["services"]["embedding"]    = await embedding_service.health_check()
    return health_status
```

**触发条件：** ChromaDB、LLM、Embedding 任一服务响应超时（默认无超时限制）。  
**潜在后果：**
- 监控系统（Prometheus、K8s Liveness Probe）轮询 `/health` 时将被下游超时拖住
- 健康的 Pod 因 `/health` 超时被误判为宕机并重启 → 触发级联重启
- 重启风暴下整个集群雪崩

**修复方向：**
```python
result = await asyncio.wait_for(service.health_check(), timeout=2.0)
```

---

## FP-03 生产密钥硬编码默认值

**级别：** 🔴 CRITICAL  
**文件：** `services/main-app/app/core/config.py:34-47`

```python
SECRET_KEY: str = Field(
    default="your-secret-key-change-in-production",  # ← 弱密钥
    env="SECRET_KEY"
)
DATABASE_URL: str = Field(
    default="postgresql://user:password@localhost/compliance_assistant",  # ← 明文密码
    env="DATABASE_URL"
)
```

同样存在于 `docker-compose.yml:54`：
```yaml
- SECRET_KEY=your-secret-key-change-in-production
- POSTGRES_PASSWORD=langchain123
```

**触发条件：** 运维人员未覆盖环境变量直接启动（常见于初次部署）。  
**潜在后果：**
- JWT 签名密钥可预测，攻击者可伪造任意用户 Token
- 数据库凭据暴露在代码仓库，一旦 repo 泄露即可直接访问生产数据库
- ChromaDB Token 为 `test-token`，无保护

**修复方向：** 启动时校验关键 secrets，若为默认值则拒绝启动：
```python
if settings.SECRET_KEY == "your-secret-key-change-in-production":
    raise RuntimeError("SECRET_KEY must be set in production")
```

---

## FP-04 LLM 扩展循环潜在 OOM 与费用爆炸

**级别：** 🟠 HIGH  
**文件：** `services/main-app/app/chains/compliance_rag_chain.py:721-763`

```python
expanded_answer = answer
while current_count < min_words and expansion_attempts < max_attempts:
    expansion_attempts += 1
    # 每次将旧内容 + 新内容拼接
    expanded_answer = f"{expanded_answer}\n\n{expanded_content}"  # 指数级增长
    current_count = self._count_chinese_words(expanded_answer)
```

- `min_words = 5000`（`COMPLIANCE_MIN_WORD_COUNT`）
- 每次追加 `max_tokens=4000` 的 LLM 输出
- 3 次叠加后 prompt 可达 **12,000+ token**

**触发条件：** 合规模式开启，模型每次生成的字数不足目标值。  
**潜在后果：**
- 上下文窗口溢出，触发 LLM API 报错
- 每次请求最多调用 LLM **4 次**，费用 4 倍放大
- 内存中字符串无限拼接，大并发下 OOM

**修复方向：** 单次生成时直接传入目标字数要求，而非循环追加。

---

## FP-05 文件上传全量读入内存

**级别：** 🟠 HIGH  
**文件：** `services/main-app/app/api/v1/documents.py:119`

```python
content = await file.read()   # ← 将整个文件读入内存
file_size = len(content)
# 验证通过后再 seek(0) 重新传给 service
await file.seek(0)
```

**触发条件：** 用户上传大文件（接近 50MB 上限）。  
**潜在后果：**
- 并发 10 个 50MB 上传 = 500MB 内存压力
- 若后续处理链也保留 bytes 对象，实际内存翻倍
- 没有流式读取，无法 early-exit 大文件

**修复方向：** 使用流式读取 + 即时写磁盘，验证 `Content-Length` header 而非先读后验。

---

## FP-06 登录接口无暴力破解防护

**级别：** 🟠 HIGH  
**文件：** `services/main-app/app/api/v1/auth.py:95`

```python
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # 无失败计数、无账号锁定、无验证码
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect credentials")
```

全局限速（`app/middleware/rate_limit.py`）仅配置 **60 次/分钟**（按 IP），对于分布式爆破毫无阻止效果。  
**潜在后果：** 无限次密码尝试，弱密码账户可被穷举破解。

---

## FP-07 WebSocket 连接无心跳超时（内存泄漏）

**级别：** 🟠 HIGH  
**文件：** `services/main-app/app/api/v1/audit_websocket.py:33`

```python
while True:
    data = await websocket.receive_text()   # ← 无超时，断网客户端永久挂起
    ...
except WebSocketDisconnect:
    break
```

**触发条件：** 客户端网络中断但未发送关闭帧（移动端网络切换、NAT 超时等常见场景）。  
**潜在后果：**
- 僵尸连接永久占用内存和连接槽
- `audit_websocket_manager` 中的连接集合无限增长
- 长时间运行后服务器 fd 耗尽

**修复方向：** 加 `asyncio.wait_for(websocket.receive_text(), timeout=30)` + 定期 ping/pong。

---

## FP-08 启动脚本依赖 `sleep` 而非就绪检查

**级别：** 🟠 HIGH  
**文件：** `start-system.sh:252,258`、`deployment/scripts/start-ubuntu-services.sh`（15+ 处）

```bash
docker-compose up -d postgres
sleep 5          # ← 固定等待，慢机器/冷启动必然失败
docker-compose up -d redis
sleep 3
```

**触发条件：** 机器负载高、镜像首次拉取、磁盘 I/O 慢。  
**潜在后果：**
- Backend 在 postgres 未就绪时启动，数据库连接池初始化失败，服务直接 crash
- `sleep 5` 在 CI/低配服务器上必然不够，部署失败率高

**修复方向：** 用 `pg_isready` 轮询替代 sleep：
```bash
until pg_isready -h localhost -U langchain; do sleep 1; done
```

---

## FP-09 级联异常吞没（Swallowed Exception）

**级别：** 🟡 MEDIUM  
**文件：** `services/main-app/app/agents/tools/analysis_tools.py:66,186,328,461`  
`services/main-app/app/api/v1/audit_maintenance.py`（16 处）  

典型模式：
```python
try:
    result = await some_tool.execute(input)
    return result
except Exception as e:
    logger.error(f"Tool execution failed: {e}")
    return {"error": str(e), "result": None}  # ← 降级为空结果，调用方无感
```

**潜在后果：**
- 工具静默失败，Agent 收到空结果后继续运行，最终返回低质量答案
- 无法区分"未找到数据"和"工具崩溃"两种情况
- 错误监控无法触发告警（HTTP 状态码仍为 200）

---

## FP-10 Redis 初始化失败静默降级

**级别：** 🟡 MEDIUM  
**文件：** `services/main-app/app/main.py:68-71`

```python
try:
    await message_broker.initialize()
except Exception as e:
    logger.warning(f"WebSocket message broker initialization failed: {e}")
    # 继续运行，但 WebSocket 功能完全不可用
```

**潜在后果：**
- 所有 WebSocket 推送静默失败，用户不知道实时功能已失效
- 监控系统看到的是"健康"状态，实际 WebSocket 功能已降级
- 前端可能无限等待推送事件

---

## FP-11 全局可变状态竞态（Embedding 模型）

**级别：** 🟡 MEDIUM  
**文件：** `services/embedding-service/app.py:26-51`

```python
embedding_model = None
model_lock = None   # ← 定义了但从未使用

async def lifespan(app):
    global embedding_model
    embedding_model = EmbeddingModel()
    await embedding_model.initialize()

@app.post("/embeddings")
async def create_embeddings(request):
    embeddings = await embedding_model.embed(request.texts)  # ← 无锁访问全局对象
```

**潜在后果：** 若未来增加动态热更换模型逻辑，无 lock 保护会引发竞态，导致部分请求使用未初始化模型。

---

## FP-12 ChromaDB 无认证 Token 轮换机制

**级别：** 🟡 MEDIUM  
**文件：** `docker-compose.yml:115`

```yaml
- CHROMA_SERVER_AUTH_CREDENTIALS=test-token   # ← 固定弱 Token
```

**潜在后果：** 在内网中任何能访问 :8005 端口的服务均可无限制读写向量库，数据泄露风险。

---

## FP-13 日志无轮转配置（磁盘耗尽）

**级别：** 🟡 MEDIUM  
**文件：** 全项目

- `start-system.sh` 通过 `nohup` 将日志写入 `logs/*.log`，无大小限制
- `structlog` 配置中无 `RotatingFileHandler`
- Nginx 容器日志无 `--log-opt max-size` 限制

**触发条件：** 服务高频请求或错误风暴。  
**潜在后果：** 磁盘写满 → 所有服务 I/O 报错 → 全站崩溃。

---

## FP-14 LLM 健康检查调用真实 LLM

**级别：** 🟡 MEDIUM  
**文件：** `services/main-app/app/services/llm_service.py`

```python
async def health_check(self):
    # 调用真实 LLM 发送测试请求以判断是否可用
    response = await self.llm.ainvoke("test")
```

**潜在后果：**
- `/health` 接口变成"收费接口"：每次健康检查都消耗 Token
- LLM 服务慢时健康检查超时，引发 FP-02 的级联问题
- Prometheus 30s 轮询 × 多副本 = 持续 LLM 调用开销

---

## FP-15 无熔断器（Circuit Breaker）

**级别：** 🟡 MEDIUM  
**文件：** 全项目

项目没有引入任何熔断机制（无 `pybreaker`、无自定义 CircuitBreaker）。调用链：

```
main-app → embedding-service → （挂死）
         → reranking-service → （挂死）
         → ChromaDB          → （挂死）
```

**潜在后果：** 任一下游服务故障时，请求持续堆积在 main-app，最终 worker 线程池耗尽，整体雪崩。

---

## FP-16 文档处理队列无优先级与限流

**级别：** 🔵 LOW  
**文件：** `services/main-app/app/tasks/document_processor.py`

```python
retry_count: int = 0   # ← 有重试计数，但无上限校验
```

**潜在后果：** 大文件处理占满队列，小文档长时间等待，无饥饿保护。

---

## FP-17 `asyncio.sleep(0.01)` 伪流式

**级别：** 🔵 LOW  
**文件：** `services/main-app/app/chains/compliance_rag_chain.py:626`

```python
for char in answer:
    yield char
    await asyncio.sleep(0.01)   # ← 假流式，所有内容已生成完毕才开始"流"
```

**潜在后果：** 用户感知延迟与实际延迟一致，流式体验完全失效，且增加了不必要的事件循环切换开销。

---

## FP-18 密码验证无常数时间比对

**级别：** 🔵 LOW  
**文件：** `services/main-app/app/api/v1/auth.py`

需确认密码比对是否使用 `passlib` 的 `verify`（常数时间）而非字符串 `==`（时序攻击）。当前 import 了 `passlib[bcrypt]`，如果正确使用则无问题，但需排查所有 token 比对路径。

---

## 汇总矩阵

| ID | 模式名称 | 文件 | 级别 | 核心影响 |
|----|----------|------|------|----------|
| FP-01 | 同步阻塞 HTTP（无超时） | `compliance_rag_chain.py:226` | 🔴 CRITICAL | 事件循环阻塞，服务崩溃 |
| FP-02 | 健康检查无超时保护 | `main.py:178` | 🔴 CRITICAL | 级联重启，集群雪崩 |
| FP-03 | 生产密钥硬编码 | `config.py:34`，`docker-compose.yml` | 🔴 CRITICAL | JWT 伪造，数据库入侵 |
| FP-04 | LLM 扩展循环 OOM | `compliance_rag_chain.py:722` | 🟠 HIGH | 内存溢出，费用爆炸 |
| FP-05 | 文件全量读入内存 | `documents.py:119` | 🟠 HIGH | 高并发 OOM |
| FP-06 | 登录无暴力破解防护 | `auth.py:95` | 🟠 HIGH | 账户被穷举 |
| FP-07 | WebSocket 无心跳超时 | `audit_websocket.py:33` | 🟠 HIGH | 连接泄漏，fd 耗尽 |
| FP-08 | 启动依赖 sleep 硬等待 | `start-system.sh:252` | 🟠 HIGH | 部署必然失败率高 |
| FP-09 | 异常吞没降级 | `analysis_tools.py`，`audit_maintenance.py` | 🟡 MEDIUM | 静默故障，难以排查 |
| FP-10 | Redis 失败静默继续 | `main.py:68` | 🟡 MEDIUM | WebSocket 功能隐性失效 |
| FP-11 | 全局状态无锁保护 | `embedding-service/app.py:26` | 🟡 MEDIUM | 竞态条件 |
| FP-12 | ChromaDB 弱 Token | `docker-compose.yml:115` | 🟡 MEDIUM | 向量库未授权访问 |
| FP-13 | 日志无轮转 | 全项目 | 🟡 MEDIUM | 磁盘写满，全站崩溃 |
| FP-14 | 健康检查消耗真实 LLM | `llm_service.py` | 🟡 MEDIUM | Token 浪费，慢检查雪崩 |
| FP-15 | 无熔断器 | 全项目 | 🟡 MEDIUM | 下游故障拖垮全链路 |
| FP-16 | 文档队列无优先级 | `document_processor.py` | 🔵 LOW | 小任务饥饿 |
| FP-17 | 伪流式实现 | `compliance_rag_chain.py:626` | 🔵 LOW | 流式体验失效 |
| FP-18 | Token 比对时序安全 | `auth.py` | 🔵 LOW | 潜在时序攻击 |

---

## 修复优先级建议

### 第一优先（本周）
1. **FP-03** — 加启动断言拒绝弱密钥，轮换所有默认 Token
2. **FP-01** — `CustomEmbeddings` 改为 `httpx.AsyncClient(timeout=30)`
3. **FP-02** — 所有 `health_check()` 调用加 `asyncio.wait_for(..., timeout=2.0)`

### 第二优先（本月）
4. **FP-07** — WebSocket 加 ping/pong + 30s 接收超时
5. **FP-06** — 登录失败计数 + 5 次锁定 15 分钟
6. **FP-08** — 所有 `sleep N` 替换为 `wait-for` 就绪探针
7. **FP-13** — 配置 `logrotate` 或 Docker `--log-opt max-size=100m`

### 第三优先（季度内）
8. **FP-04** — 重构扩展逻辑，单次 prompt 传入目标字数
9. **FP-15** — 引入 `pybreaker` 熔断器包裹所有下游调用
10. **FP-05** — 文件上传改为流式读取 + `Content-Length` 预校验
