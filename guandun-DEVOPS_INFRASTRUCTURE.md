# Drass DevOps 基础设施文档

> 生成日期：2026-04-26

---

## 目录

1. [整体架构概览](#整体架构概览)
2. [部署环境矩阵](#部署环境矩阵)
3. [容器化方案](#容器化方案)
4. [服务编排](#服务编排)
5. [网络与反向代理](#网络与反向代理)
6. [数据持久化](#数据持久化)
7. [监控与可观测性](#监控与可观测性)
8. [日志体系](#日志体系)
9. [健康检查](#健康检查)
10. [资源限制](#资源限制)
11. [密钥与环境变量管理](#密钥与环境变量管理)
12. [启停运维脚本](#启停运维脚本)
13. [Systemd 服务管理](#systemd-服务管理)
14. [LLM 推理服务](#llm-推理服务)
15. [CI/CD 与部署流水线](#cicd-与部署流水线)
16. [安全加固](#安全加固)
17. [当前已知风险](#当前已知风险)

---

## 整体架构概览

```
                  ┌─────────────────────────────────────────────────────┐
                  │                   外部访问层                          │
                  │         Nginx（:80/:443）HTTP→HTTPS 重定向            │
                  └───────────────────────┬─────────────────────────────┘
                                          │ TLS 1.2/1.3
                          ┌───────────────┴───────────────┐
                          │                               │
                   ┌──────▼──────┐               ┌───────▼──────┐
                   │ Frontend    │               │  main-app    │
                   │ React:5173  │               │ FastAPI:8000 │
                   └─────────────┘               └──────┬───────┘
                                                        │
              ┌─────────────────────────────────────────┼───────────┐
              │                         │               │           │
       ┌──────▼──────┐         ┌────────▼──────┐ ┌─────▼────┐ ┌───▼────────┐
       │  Embedding  │         │  Reranking    │ │ Doc Proc │ │ LLM        │
       │  Svc:8002   │         │  Svc:8004     │ │ :5003    │ │ Gateway    │
       └──────┬──────┘         └───────┬───────┘ └──────────┘ │ :8003      │
              │                        │                        └────┬───────┘
              └───────────┬────────────┘                            │
                          ▼                              ┌──────────▼──────────┐
                  ┌───────────────┐                      │ vLLM / Qwen3-8B-MLX │
                  │  Redis :6379  │                      │ :8001               │
                  └───────────────┘                      └─────────────────────┘
              ┌───────────────────────┐
              │ PostgreSQL :5432      │
              │ ChromaDB   :8005      │
              └───────────────────────┘
```

---

## 部署环境矩阵

| 环境 | 描述 | LLM | Embedding | Vector Store | 编排方式 |
|------|------|-----|-----------|--------------|----------|
| **本地开发（macOS/Apple Silicon）** | 开发调试 | Qwen3-8B-MLX（MLX） | sentence-transformers 本地 | ChromaDB 本地文件 | `start-system.sh` 直接进程 |
| **本地 Docker（docker-local）** | 一键容器化 | Qwen3-8B-MLX（宿主机） | sentence-transformers 容器 | ChromaDB 容器 | `docker-compose.yml` |
| **Ubuntu 生产（AMD GPU）** | 服务器部署 | vLLM + Qwen2.5-8B-Instruct（CUDA） | vLLM + Qwen3-Embedding-8B | ChromaDB 持久化 | systemd + docker-compose.prod.yml |
| **AWS 生产** | 云原生部署 | OpenRouter（云端多模型） | OpenAI text-embedding-ada-002 | Pinecone | ECS + ALB |

---

## 容器化方案

### Dockerfile 策略对比

| 服务 | 构建策略 | 基础镜像 | 特殊处理 |
|------|----------|----------|----------|
| `main-app` | **多阶段构建**（builder → runtime） | python:3.11-slim | 非 root 用户（appuser:1000）；安装 tesseract-ocr（中英文） |
| `reranking-service` | **3 阶段构建**（base → dependencies → app） | python:3.11-slim | 清华 pip 镜像加速；非 root 用户（reranker:1000）；HuggingFace 缓存目录 |
| `doc-processor` | 单阶段 | python:3.11-slim | 清华 apt 镜像；poppler-utils + tesseract；OCR 仅英文（生产追加中文包） |
| `embedding-service` | 单阶段 | python:3.11-slim | 模型文件挂载至 `/app/models` |
| `llm-gateway` | 单阶段 | python:3.11-slim | 4 worker uvicorn 启动 |
| `scheduler` | 单阶段 | python:3.11-slim | 安装系统 cron |
| 根目录 `Dockerfile` | 单阶段（脚本/工具用） | python:3.11-slim | 非 root 用户（app）；用于 deploy/validate 脚本 |

### 镜像加速配置

reranking-service 和 doc-processor 使用国内镜像加速：

```
apt 源:  mirrors.tuna.tsinghua.edu.cn/debian/
pip 源:  pypi.tuna.tsinghua.edu.cn/simple/
         mirrors.aliyun.com/pypi/simple/
         pypi.douban.com/simple/
```

---

## 服务编排

### 开发环境 `docker-compose.yml`

**网络：** 单一 `langchain-network`（bridge 模式），所有服务内部通信通过服务名寻址。

**服务启动依赖链：**

```
postgres ◄─────── main-app ◄──── frontend
redis    ◄─────── main-app
         ◄─────── embedding-service
         ◄─────── reranking-service（condition: service_started）
         ◄─────── llm-gateway
chromadb ◄─────── main-app
embedding-service ◄─ main-app
reranking-service ◄─ main-app
doc-processor     ◄─ main-app
```

**Docker Profiles（按需启动）：**

| Profile | 包含服务 | 启动命令 |
|---------|----------|----------|
| 默认（无 profile） | frontend、main-app、embedding、reranking、doc-processor、llm-gateway、postgres、redis、chromadb | `docker-compose up -d` |
| `production` | + nginx | `docker-compose --profile production up -d` |
| `monitoring` | + prometheus、grafana | `docker-compose --profile monitoring up -d` |

### 生产环境 `docker-compose.prod.yml`

生产环境额外包含：

| 服务 | 镜像 | 端口 | 说明 |
|------|------|------|------|
| `vllm-service` | vllm/vllm-openai:latest | :8001 | GPU 推理，`CUDA_VISIBLE_DEVICES=0` |
| `embedding-service` | vllm/vllm-openai:latest | :8010 | GPU 嵌入，`CUDA_VISIBLE_DEVICES=1` |
| `reranker-service` | vllm/vllm-openai:latest | :8012 | GPU 重排，`CUDA_VISIBLE_DEVICES=2` |
| `loki` | grafana/loki:latest | :3100 | 日志聚合 |
| `promtail` | grafana/promtail:latest | — | 日志采集代理 |

> 生产环境 main-app 监听 **:8888**（非开发环境的 :8000）。

---

## 网络与反向代理

### Nginx 配置要点

| 功能 | 配置 |
|------|------|
| HTTP→HTTPS 强制跳转 | `return 301 https://$host$request_uri` |
| TLS 版本 | TLSv1.2、TLSv1.3 |
| TLS 密码套件 | ECDHE-RSA-AES128/256-GCM-SHA256/384 |
| HTTP/2 | 已启用（`listen 443 ssl http2`） |
| SSL Session 缓存 | `shared:SSL:10m`，超时 10 分钟 |
| 安全响应头 | X-Frame-Options: DENY、X-Content-Type-Options: nosniff、X-XSS-Protection、HSTS（max-age=31536000） |
| Gzip 压缩 | 已启用，最小 1024B，级别 6，覆盖 text/css/js/json/svg |
| 客户端最大上传 | `client_max_body_size 100M` |
| API 限速 | `limit_req_zone` 10r/s（burst=20），Web 30r/s（burst=50） |
| WebSocket 支持 | `Upgrade` + `Connection: upgrade`（HTTP/1.1） |
| 静态资源缓存 | js/css/图片 `expires 1y; Cache-Control: public, immutable` |
| 上游 keepalive | `keepalive 32` |
| 超时配置 | connect/send/read 均为 30s |

---

## 数据持久化

### Docker Named Volumes

| Volume | 挂载服务 | 用途 |
|--------|----------|------|
| `postgres_data` | PostgreSQL | 关系型数据（`/var/lib/postgresql/data`） |
| `redis_data` | Redis | AOF 持久化数据（`/data`） |
| `chroma_data` | ChromaDB | 向量数据（`/chroma/chroma`） |
| `prometheus_data` | Prometheus | 指标时序数据（`/prometheus`） |
| `grafana_data` | Grafana | 仪表盘配置（`/var/lib/grafana`） |

### Bind Mounts（宿主机目录映射）

| 宿主机路径 | 容器路径 | 服务 | 用途 |
|-----------|----------|------|------|
| `./data/uploads` | `/app/uploads` | main-app | 用户上传文件 |
| `./data/documents` | `/app/documents` | doc-processor | 待处理文档 |
| `./data/processed` | `/app/processed` | doc-processor | 处理结果 |
| `./models/embeddings` | `/app/models` | embedding-service | 嵌入模型缓存 |
| `./models/reranking` | `/app/model_cache` | reranking-service | 重排模型缓存 |
| `./logs/reranking` | `/app/logs` | reranking-service | 服务日志 |
| `./nginx/nginx.conf` | `/etc/nginx/nginx.conf` | nginx | Nginx 配置 |
| `./nginx/ssl` | `/etc/nginx/ssl` | nginx | TLS 证书 |
| `./scripts/init.sql` | `/docker-entrypoint-initdb.d/init.sql` | postgres | 数据库初始化 SQL |

### Redis 持久化

```bash
redis-server --appendonly yes
# 生产环境追加密码：
redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
```

---

## 监控与可观测性

### Prometheus 抓取配置

| Job | 目标 | 抓取间隔 | 指标路径 |
|-----|------|----------|----------|
| `prometheus` | localhost:9090 | 15s | `/metrics` |
| `drass-app` | drass-app:8000 | 30s | `/metrics` |
| `postgres` | postgres:5432 | 30s | `/metrics`（需 postgres_exporter） |
| `redis` | redis:6379 | 30s | `/metrics`（需 redis_exporter） |
| `nginx` | nginx:80 | 30s | `/nginx_status` |
| `node` | host.docker.internal:9100 | 30s | 宿主机 Node Exporter |
| `docker` | host.docker.internal:9323 | 30s | Docker 守护进程指标 |

**数据保留策略：** 200h / 10GB（二者取其先）

**外部标签：**
```yaml
environment: production
application: drass
version: 1.0.0
```

**告警：** 已配置 Alertmanager（:9093），规则文件在 `rules/*.yml`。

### Grafana

| 配置项 | 值 |
|--------|-----|
| 数据源 | Prometheus（http://prometheus:9090，代理模式） |
| 日志数据源（生产） | Loki（http://loki:3100） |
| Dashboard 自动加载 | provisioning 目录，更新间隔 10s |
| 插件 | redis-datasource |
| 生产管理员密码 | `${GRAFANA_PASSWORD}`（环境变量注入） |

### 生产日志栈（PLG）

```
服务日志（/var/log/*.log）
    └──► Promtail（采集）
             └──► Loki:3100（聚合存储）
                      └──► Grafana（查询展示）
```

---

## 日志体系

### 应用日志

| 服务 | 日志格式 | 日志路径 |
|------|----------|----------|
| main-app | 结构化 JSON（structlog） | `logs/backend.log` |
| reranking-service | 结构化 JSON（structlog） | `logs/reranking/` |
| llm-gateway | JSON | stdout |
| scheduler | loguru | `logs/` |
| 本地 LLM | 文本 | `logs/llm.log` |
| embedding-service | 文本 | `logs/embedding.log` |
| frontend | 文本 | `logs/frontend.log` |

### Nginx 访问日志格式

```nginx
log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                '$status $body_bytes_sent "$http_referer" '
                '"$http_user_agent" "$http_x_forwarded_for"';
```

---

## 健康检查

| 服务 | 检查命令 | 间隔 | 超时 | 重试 | 启动缓冲 |
|------|----------|------|------|------|----------|
| `postgres` | `pg_isready -U langchain` | 10s | 5s | 5 | — |
| `redis` | `redis-cli ping` | 10s | 5s | 5 | — |
| `main-app` | `curl -f localhost:8000/health` | 30s | 10s | 3 | 5s |
| `reranking-service` | `curl -f localhost:8002/health` | 30s | 10s | 3 | **60s** |
| `llm-gateway` | `requests.get('localhost:8003/health')` | 30s | 10s | 3 | 5s |
| `vllm-service`（生产） | `curl -f localhost:8001/v1/models` | 30s | 10s | 3 | **60s** |
| `nginx`（生产） | `wget --spider localhost/health` | 30s | 10s | 3 | — |
| `main-app`（生产） | `curl -f localhost:8888/health` | 30s | 10s | 3 | 40s |

---

## 资源限制

### 当前已配置资源限制（Docker Deploy）

| 服务 | CPU 上限 | 内存上限 | CPU 预留 | 内存预留 |
|------|----------|----------|----------|----------|
| `reranking-service` | 1.0 核 | 2 GB | 0.5 核 | 512 MB |

> 其余服务暂未配置资源限制，建议生产环境补充。

### 生产 AWS 模板资源规格

| 服务 | CPU 请求 | 内存请求 | CPU 上限 | 内存上限 |
|------|----------|----------|----------|----------|
| API（3 副本） | 2 核 | 4 GB | — | — |
| Frontend（2 副本） | 1 核 | 2 GB | — | — |
| 整体（ECS Task） | 4 核 | 8 GB | 8 核 | 16 GB |
| 存储（EBS） | — | — | — | 100 GB（3000 IOPS，加密） |

---

## 密钥与环境变量管理

### 变量分类

| 类别 | 变量名 | 说明 |
|------|--------|------|
| **LLM** | `LLM_PROVIDER` `LLM_MODEL` `LLM_API_KEY` `OPENAI_API_BASE` `OPENROUTER_API_KEY` | LLM 提供商配置 |
| **数据库** | `DATABASE_URL` `DB_PASSWORD` | PostgreSQL 连接串 |
| **缓存** | `REDIS_URL` `REDIS_PASSWORD` | Redis 连接 |
| **安全** | `SECRET_KEY` `JWT_SECRET_KEY` `JWT_ALGORITHM` `ENCRYPTION_KEY` | 签名与加密 |
| **向量库** | `VECTOR_STORE_TYPE` `CHROMA_SERVER_HOST` `CHROMA_SERVER_PORT` | ChromaDB/Pinecone |
| **Embedding** | `EMBEDDING_API_BASE` `EMBEDDING_MODEL` `EMBEDDING_PROVIDER` | 嵌入服务 |
| **Reranking** | `RERANKING_ENABLED` `RERANKING_API_BASE` `RERANKING_MODEL` | 重排序服务 |
| **功能开关** | `ENABLE_STREAMING` `ENABLE_AGENT` `ENABLE_MEMORY` | Feature Flags |
| **监控** | `GRAFANA_PASSWORD` | Grafana 管理密码 |
| **AWS（生产）** | `AWS_ACCOUNT_ID` `AWS_REGION` `RDS_PASSWORD` `ELASTICACHE_AUTH_TOKEN` `PINECONE_API_KEY` | 云服务凭证 |

### 管理机制

| 环境 | 管理方式 |
|------|----------|
| 本地开发 | `.env` 文件（`.gitignore` 排除，`env.example` 提供模板） |
| Docker Compose | `environment:` 字段 + `${VAR:-default}` 语法（支持默认值） |
| Ubuntu 生产 | systemd `Environment=` 或宿主机 `.env` 文件 |
| AWS | AWS Secrets Manager（`secrets_manager: aws-secrets`） |

> **安全警告：** `docker-compose.yml` 中 `SECRET_KEY=your-secret-key-change-in-production` 为明文占位符，生产环境**必须替换**。ChromaDB Token 当前为 `test-token`，**必须轮换**。

---

## 启停运维脚本

### 主要脚本清单

| 脚本 | 用途 | 说明 |
|------|------|------|
| `start-system.sh` | 一键完整启动 | 按顺序启动所有服务，含健康等待 |
| `stop-services.sh` | 停止所有服务 | PID 文件 → 端口 kill → 进程名 pkill 三重保障 |
| `quick-start.sh` | 快速启动 | 精简版启动 |
| `start-frontend-only.sh` | 仅启动前端 | 用于前端独立调试 |
| `start-system-optimized.sh` | 优化启动 | 内存/性能优化版本 |
| `scripts/deploy.py` | Python 部署脚本 | 可配置化部署 |
| `deployment/scripts/start-ubuntu-services.sh` | Ubuntu 服务启动 | 生产服务器专用 |
| `deployment/scripts/stop-ubuntu-services.sh` | Ubuntu 服务停止 | 生产服务器专用 |
| `deployment/production/deploy-production.sh` | 生产全量部署 | 含前置检查、构建、启动 |
| `deployment/production/start-monitoring.sh` | 启动监控栈 | Prometheus + Grafana + Loki |
| `scripts/build-optimized.sh` | 优化镜像构建 | BuildKit 缓存加速 |
| `scripts/build-reranking.sh` | Reranking 镜像构建 | 多阶段构建专用 |

### `start-system.sh` 启动顺序

```
1. cleanup_existing   → 清理残留进程（按端口 kill）+ docker-compose down
2. setup_environment  → 生成 .env（如不存在）+ 加载环境变量
3. start_infrastructure → Docker: postgres → redis → chromadb（等待就绪）
4. start_microservices → embedding（直接进程）→ reranking（Docker）→ doc-processor（Docker）
5. start_llm          → qwen3_api_server.py（nohup 后台）
6. start_backend      → venv + uvicorn app.main:app --reload（nohup 后台）
7. start_frontend     → npm run dev（nohup 后台）
8. test_system        → curl 健康检查所有服务
9. show_status        → 输出所有服务 URL
```

### PID 文件管理

进程 PID 写入 `.pids/` 目录：
- `.pids/embedding.pid`
- `.pids/llm.pid`
- `.pids/backend.pid`
- `.pids/frontend.pid`

---

## Systemd 服务管理

生产 Ubuntu 服务器使用 systemd 管理长驻服务：

### `drass-api.service`（后端 API）

```ini
[Unit]
After=network.target postgresql.service redis.service

[Service]
Type=simple
User=qwkj
WorkingDirectory=/home/qwkj/drass/services/main-app
Environment="PATH=/home/qwkj/.pyenv/shims:..."
Environment="NO_PROXY=localhost,127.0.0.1,::1,0.0.0.0"
ExecStart=/home/qwkj/drass/services/main-app/start_api_no_proxy.sh
Restart=on-failure
RestartSec=10
```

### `drass-frontend.service`（前端）

```ini
[Unit]
After=network.target

[Service]
Type=simple
User=qwkj
WorkingDirectory=/home/qwkj/drass
ExecStart=/home/qwkj/drass/start-frontend-only.sh
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
```

**常用 systemd 命令：**
```bash
systemctl enable drass-api drass-frontend   # 开机自启
systemctl start drass-api drass-frontend    # 启动
systemctl status drass-api                  # 查看状态
journalctl -u drass-api -f                  # 实时日志
systemctl restart drass-api                 # 重启
```

---

## LLM 推理服务

### 本地推理（开发/macOS）

| 方案 | 实现 | 优势 |
|------|------|------|
| **MLX-LM**（首选） | `qwen3_api_server.py`（Flask + mlx_lm） | Apple Silicon 原生加速 |
| **Ollama** | `ollama serve` + Qwen2.5:7b | 易用，跨平台 |
| **LM Studio** | `scripts/deploy_lmstudio.sh` | GUI 界面 |

MLX 服务器配置：
```bash
mlx_lm.server --model ~/.lmstudio/models/Qwen/Qwen3-8B-MLX-bf16 --port 8001
```

### 生产 GPU 推理（Ubuntu + AMD/CUDA）

| 服务 | 模型 | GPU | 内存利用率 |
|------|------|-----|------------|
| vLLM LLM | Qwen2.5-8B-Instruct | GPU:0 | 80% |
| vLLM Embedding | Qwen3-Embedding-8B | GPU:1 | 60% |
| vLLM Reranker | Qwen3-Reranker-8B | GPU:2 | 40% |

vLLM 全局参数：
```
--dtype bfloat16
--max-model-len 4096（LLM）/ 8096（Embedding）
--api-key 123456
```

### 云端推理（AWS）

| 用途 | 服务 | 模型 |
|------|------|------|
| 文本生成 | OpenRouter | gpt-4-turbo |
| Embedding | OpenAI | text-embedding-ada-002（1536 维） |
| Reranking | Cohere | rerank-english-v2.0 |

---

## CI/CD 与部署流水线

当前项目**无正式 CI/CD 平台**（无 GitHub Actions / GitLab CI 配置文件），部署依赖以下脚本：

### 部署脚本体系

```
deployment/
├── scripts/
│   ├── configure.py          # 交互式配置生成器（硬件检测 + 模板渲染）
│   ├── configure_simple.py   # 简化版配置生成
│   ├── deploy.py             # 主部署脚本
│   ├── validate.py           # 部署前校验
│   ├── install-dependencies.sh  # 系统依赖安装
│   ├── setup-venv.sh         # Python 虚拟环境
│   ├── build-frontend-prod.sh   # 前端生产构建
│   ├── restart-ubuntu-services.sh  # Ubuntu 服务重启
│   ├── test-all-services.sh  # 全量健康测试
│   └── utils/
│       ├── config_loader.py      # 配置加载器
│       ├── config_models.py      # 配置数据模型（Pydantic）
│       └── hardware_detector.py  # 硬件自动检测
├── configs/
│   ├── presets/
│   │   ├── dev-macos.yaml              # macOS 开发预设
│   │   ├── docker-local.yaml           # 本地 Docker 预设
│   │   └── ubuntu-amd-production.yaml  # Ubuntu AMD GPU 生产预设
│   └── templates/
│       ├── aws.yaml            # AWS 部署模板
│       ├── docker-compose.yaml # Docker Compose 模板
│       ├── local-gpu.yaml      # 本地 GPU 模板
│       └── ubuntu-amd-gpu.yaml # Ubuntu AMD GPU 模板
└── production/
    ├── deploy-production.sh    # 生产全量部署（15KB）
    ├── deploy.sh               # 简化部署
    └── docker-compose.prod.yml # 生产 Compose 文件
```

### 硬件自动检测（`hardware_detector.py`）

部署配置脚本可自动识别：
- GPU 类型（NVIDIA CUDA / AMD ROCm / Apple Metal）
- 可用显存大小
- CPU 核数与内存
- 据此自动选择推荐的部署预设

---

## 安全加固

### 已实施措施

| 层次 | 措施 |
|------|------|
| **容器** | main-app 使用非 root 用户（appuser:1000）；reranking 使用非 root（reranker:1000） |
| **TLS** | Nginx 强制 HTTPS，TLSv1.2/1.3，HSTS |
| **HTTP 安全头** | X-Frame-Options: DENY、nosniff、XSS-Protection |
| **API 限速** | Nginx `limit_req_zone`：API 10r/s，Web 30r/s |
| **认证** | JWT（HS256），FastAPI `python-jose` |
| **密码** | bcrypt 哈希（passlib） |
| **Redis 生产** | requirepass 密码保护 |
| **ChromaDB** | Token 认证（`AUTHORIZATION` Header） |

### 待加固项（安全风险）

| 风险级别 | 问题 | 建议 |
|----------|------|------|
| **CRITICAL** | `SECRET_KEY=your-secret-key-change-in-production` 明文占位符 | 生成高熵随机密钥并注入 |
| **CRITICAL** | ChromaDB Token 为 `test-token` | 生产环境轮换为强 Token |
| **HIGH** | 数据库密码 `langchain123` 硬编码在 `docker-compose.yml` | 改用环境变量注入 |
| **HIGH** | vLLM API Key `123456` 过弱 | 生产环境使用高强度密钥 |
| **HIGH** | Nginx CORS 配置 `Access-Control-Allow-Origin: *` | 限制为具体域名 |
| **MEDIUM** | 大多数服务无资源上限 | 补充 `deploy.resources.limits` |
| **MEDIUM** | 无正式 secrets 管理 | 开发环境引入 Vault 或 SOPS |
| **LOW** | 无自动化安全扫描（Trivy/Snyk） | 集成到部署前检查 |

---

## 当前已知风险

| 类别 | 描述 |
|------|------|
| **无 CI/CD** | 无自动化测试流水线，依赖手工脚本部署，易引入回归 |
| **无镜像仓库** | 未配置私有 Container Registry，镜像无版本管理 |
| **无 K8s** | 纯 Docker Compose 编排，无自动扩缩容、无故障自愈（除 `restart: unless-stopped`） |
| **单节点** | 所有服务运行在单台宿主机，无横向扩展设计（AWS 模板除外） |
| **数据备份** | 无自动化数据库备份策略 |
| **日志轮转** | 未配置 logrotate，长期运行可能耗尽磁盘 |
| **模型文件管理** | 模型文件通过 bind mount 挂载，无版本控制 |
