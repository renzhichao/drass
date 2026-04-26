# Drass 项目命名规范字典（Naming Rules Dictionary）

> 版本：1.0 · 日期：2026-04-26  
> 基于对项目现有代码的全量扫描，提炼出实际使用的命名模式，并对不一致处给出统一规范。

---

## 目录

1. [总体原则](#1-总体原则)
2. [Python — 后端](#2-python--后端)
   - 2.1 [模块/文件名](#21-模块文件名)
   - 2.2 [类名](#22-类名)
   - 2.3 [函数/方法名](#23-函数方法名)
   - 2.4 [变量名](#24-变量名)
   - 2.5 [常量名](#25-常量名)
   - 2.6 [私有符号](#26-私有符号)
3. [FastAPI — 路由](#3-fastapi--路由)
   - 3.1 [URL 路径](#31-url-路径)
   - 3.2 [路由函数名](#32-路由函数名)
   - 3.3 [路由文件名](#33-路由文件名)
4. [TypeScript/React — 前端](#4-typescriptreact--前端)
   - 4.1 [组件文件名](#41-组件文件名)
   - 4.2 [组件函数名](#42-组件函数名)
   - 4.3 [Hook 名](#43-hook-名)
   - 4.4 [Interface/Type 名](#44-interfacetype-名)
   - 4.5 [Redux Slice 名](#45-redux-slice-名)
   - 4.6 [前端变量/函数名](#46-前端变量函数名)
5. [环境变量](#5-环境变量)
6. [Docker & 容器](#6-docker--容器)
7. [Shell 脚本](#7-shell-脚本)
8. [日志文件](#8-日志文件)
9. [数据库/模型](#9-数据库模型)
10. [不一致问题清单](#10-不一致问题清单)
11. [快速参考卡](#11-快速参考卡)

---

## 1. 总体原则

| 原则 | 说明 |
|------|------|
| **语言一致** | 所有标识符使用**英文**，禁止拼音或中英混用 |
| **风格匹配层级** | Python → snake_case；TypeScript/React → camelCase/PascalCase；常量 → SCREAMING_SNAKE_CASE；URL → kebab-case |
| **语义优先** | 名称须能独立表达意图，禁止 `data`、`info`、`tmp` 等无语义名称 |
| **动词前缀规律** | 函数以动词开头（`get_`、`create_`、`update_`、`delete_`、`check_`、`build_`）；布尔函数以 `is_`/`has_`/`can_` 开头 |
| **后缀表达角色** | Python 类用后缀声明职责（`Service`、`Manager`、`Factory`、`Tool`、`Chain`、`Handler`）；TypeScript interface 用后缀 `Props`、`State`、`Config`、`Request`、`Response` |
| **无缩写** | 禁止自创缩写；行业通用词（`llm`、`rag`、`api`、`url`、`id`）除外 |

---

## 2. Python — 后端

### 2.1 模块/文件名

**规则：** `snake_case`，复数名词表资源模块，动词_名词表操作模块。

| 模式 | 示例 | 说明 |
|------|------|------|
| 资源（复数） | `documents.py`、`conversations.py`、`alerts.py` | API 路由文件 |
| 功能 + `_service` | `audit_service.py`、`document_service.py`、`llm_service.py` | 业务服务 |
| 功能 + `_service_enhanced` | `llm_service_enhanced.py`、`audit_service_enhanced.py` | ❌ 禁止用 `_enhanced`，应版本化或重命名 |
| 功能 + `_chain` | `compliance_rag_chain.py`、`optimized_rag_chain.py` | LangChain 链 |
| 功能 + `_tools` | `analysis_tools.py`、`document_tools.py`、`search_tools.py` | LangChain 工具集 |
| 厂商/提供商名 | `openrouter.py`、`openai_compatible.py`、`lmstudio.py` | LLM 提供商适配器 |
| 工具脚本 | `config_loader.py`、`hardware_detector.py` | 部署工具 |

**禁止：**
```
# ❌ 不一致的模式（现存问题）
audit_service.py          # 基础版
audit_service_enhanced.py # 不应加 _enhanced 后缀
vector_store.py           # 基础版
vector_store_optimized.py # 不应加 _optimized 后缀

# ✅ 正确做法：用功能差异命名，或仅保留一个版本
audit_service.py
vector_store_service.py   # 统一加 _service 后缀
```

---

### 2.2 类名

**规则：** `PascalCase`，后缀声明职责类型。

#### 后缀规范

| 后缀 | 职责 | 示例 |
|------|------|------|
| `Service` | 业务逻辑层，可被路由或其他服务调用 | `AuditService`、`ChatService`、`AuthService` |
| `Manager` | 资源生命周期管理（连接池、WebSocket 连接集合） | `AuditWebSocketManager`、`WebSocketMessageBroker` |
| `Factory` | 创建复杂对象或策略族 | `ComplianceRAGChainFactory`、`SpecializedAgentFactory` |
| `Chain` | LangChain 链实现 | `ComplianceRAGChain`、`AdaptiveRAGChain` |
| `Tool` | LangChain 工具 | `ComplianceAnalysisTool`、`DocumentSearchTool`、`WebSearchTool` |
| `Handler` | 事件/回调处理器 | `StreamingCallbackHandler`、`ErrorHandler` |
| `Middleware` | FastAPI 中间件 | `RequestIDMiddleware`、`RateLimitMiddleware` |
| `Agent` | LangChain Agent | `ComplianceAgent` |
| `Orchestrator` | 多 Agent 协调器 | `AgentOrchestrator` |
| `Scanner` | 扫描/检测类 | `VulnerabilityScanner` |
| *(无后缀)* | Pydantic 模型（请求/响应体） | `ChatMessage`、`Document`、`AuditLog` |

#### Pydantic 模型后缀规范

| 后缀 | 场景 | 示例 |
|------|------|------|
| `Request` | HTTP 请求体 | `ChatRequest`、`SearchRequest`、`BatchOptimizeRequest` |
| `Response` | HTTP 响应体 | `ChatResponse`、`AuditLogResponse`、`ScanReportResponse` |
| `Create` | 创建操作 DTO | `AuditLogCreate` |
| `Update` | 更新操作 DTO | `AuditLogUpdate` |
| `DB` | 数据库 ORM 模型 | `AuditLogDB` |
| `Base` | 共享基类 Pydantic 模型 | `AuditLogBase` |
| `Config` | 配置数据类 | `CompliancePromptConfig`、`ChromaDBOptimizationConfig` |
| `Settings` | 设置子模型 | `RerankingSettings`、`VectorStoreSettings` |
| `Input` | LangChain Tool 输入 | `ComplianceAnalysisInput`、`ChecklistInput` |

#### 枚举类命名

| 规则 | 示例 |
|------|------|
| 单数名词 + `PascalCase` | `AlertLevel`、`AuditStatus`、`AlertCategory`、`AlertSeverity` |
| 枚举值 → `SCREAMING_SNAKE_CASE` | `CRITICAL`、`HIGH`、`MEDIUM`、`LOW` |

---

### 2.3 函数/方法名

**规则：** `snake_case`，以动词开头。

#### 动词前缀词典

| 前缀 | 语义 | 示例 |
|------|------|------|
| `get_` | 查询单个或列表资源 | `get_document()`、`get_audit_logs()`、`get_current_user()` |
| `create_` | 创建新资源 | `create_access_token()`、`create_knowledge_base()` |
| `update_` | 更新已有资源 | `update_user()`、`update_monitoring_config()` |
| `delete_` | 删除资源 | `delete_document()`、`delete_knowledge_base()` |
| `upload_` | 上传文件/资源 | `upload_document()` |
| `export_` | 导出数据 | `export_audit_logs_csv()`、`export_audit_logs_json()` |
| `import_` | 导入数据 | `import_knowledge_source()` |
| `send_` | 发送消息/通知 | `send_notification()` |
| `broadcast_` | 广播消息（WebSocket） | `broadcast_websocket_message()` |
| `check_` | 验证/检查，返回 bool 或抛异常 | `check_permission()`、`check_suspicious_activity()` |
| `verify_` | 验证凭据/签名 | `verify_password()`、`verify_api_key()` |
| `validate_` | 校验数据格式/约束 | `validate_file_type()`、`validate_environment()` |
| `build_` | 构建复杂对象 | `build_prompt()`、`build_context()` |
| `generate_` | 生成内容/Token | `generate_api_key()`、`generate_security_report()` |
| `init_` / `initialize_` | 初始化服务/资源 | `init_alert_service()`、`initialize_services()` |
| `setup_` | 配置/安装 | `setup_logging()` |
| `cleanup_` / `clear_` | 清理资源 | `cleanup_old_logs()`、`clear_cache()` |
| `start_` / `stop_` | 启停服务 | `start_microservices()`、`stop_services()` |
| `load_` | 加载数据/配置 | `load_config()`、`load_model()` |
| `save_` / `store_` | 持久化 | `save_document()`、`store_embedding()` |
| `parse_` | 解析文本/文件 | `parse_document()`、`parse_config()` |
| `format_` | 格式化输出 | `format_file_context()`、`format_response()` |
| `encode_` / `decode_` | 编解码 | `decode_token()`、`encode_content()` |
| `encrypt_` / `decrypt_` | 加解密 | `encrypt_data()`、`decrypt_data()` |
| `compress_` | 压缩 | `compress_backup()`、`compress_archived_logs()` |
| `archive_` | 归档 | `archive_old_logs()` |
| `log_` | 记录日志 | `log_api_request()`、`log_error()` |
| `record_` | 记录指标 | `record_request_metrics()` |
| `handle_` | 处理事件/请求 | `handle_client_message()`、`error_handler_middleware()` |
| `process_` | 处理数据/任务 | `process_document()`、`process_query()` |
| `invoke_` / `ainvoke_` | 调用链/Agent | `ainvoke()`、`invoke_tool()` |
| `stream_` | 流式输出 | `stream_response()`、`chat_stream()` |
| `hash_` | 哈希运算 | `hash_api_key()`、`get_password_hash()` |
| `require_` | 授权守卫 | `require_role()` |
| `sample_` | 采样 | `sample_file()` |
| `apply_` | 应用配置/迁移 | `apply_migrations()` |
| `downgrade_` / `upgrade_` | 数据库迁移版本控制 | `upgrade()`、`downgrade()` |

#### 布尔返回函数

| 前缀 | 示例 |
|------|------|
| `is_` | `is_production()`、`is_development()`、`is_active()` |
| `has_` | `has_permission()`、`has_knowledge_base()` |
| `can_` | `can_access()`、`can_modify()` |

#### 异步函数

- 所有 I/O 相关函数必须声明 `async def`
- 异步版本**不加** `async_` 前缀（不写 `async_get_document`），而是直接 `async def get_document`
- LangChain 异步调用方法保留 `ainvoke` 约定（`a` 前缀为 LangChain 框架约定，不自创）

---

### 2.4 变量名

**规则：** `snake_case`，名词或名词短语。

| 类型 | 规则 | 示例 |
|------|------|------|
| 普通变量 | 名词，描述内容 | `user_id`、`file_size`、`chunk_size`、`access_token` |
| 集合变量 | 复数名词 | `documents`、`tag_list`、`base_ids` |
| 布尔变量 | `is_`/`has_`/`can_` 前缀 | `is_active`、`has_error`、`auto_process` |
| 临时循环变量 | 单字母仅限简单迭代 | `for i in range(3):`（用于计数），其余用全名 |
| 回调/依赖注入 | 与参数语义一致 | `current_user`、`form_data`、`request` |
| 服务单例 | `_service` 后缀 + 全局变量 | `document_service`、`storage_service` |

**禁止：**
```python
# ❌
d = get_document()
tmp = file.read()
res = await llm.ainvoke(q)

# ✅
document = get_document()
file_content = await file.read()
llm_response = await llm.ainvoke(query)
```

---

### 2.5 常量名

**规则：** `SCREAMING_SNAKE_CASE`，模块级声明，语义明确。

| 类别 | 示例 | 说明 |
|------|------|------|
| Prompt 模板 | `COMPLIANCE_QA_PROMPT`、`MULTI_QUERY_PROMPT`、`RISK_ASSESSMENT_PROMPT` | 所有 Prompt 常量以功能 + `_PROMPT` 结尾 |
| 配置默认值 | `DEFAULT_COMPLIANCE_CONFIG`、`EXPANSION_PROMPT` | `DEFAULT_` 前缀 |
| 安全常量 | `_WEAK_SECRET_KEY`、`_WEAK_DB_PASSWORDS` | 私有安全常量加 `_` 前缀 |
| 限流/超时 | `_FAIL_MAX`、`_RESET_TIMEOUT`、`_MAX_ATTEMPTS`、`_LOCKOUT_SECONDS` | 私有运行时常量加 `_` 前缀 |
| WebSocket 参数 | `_WS_RECEIVE_TIMEOUT`、`_WS_PING_INTERVAL` | 私有 WS 常量加 `_` 前缀 |

**禁止：**
```python
# ❌
max_attempts = 5          # 应为常量 _MAX_ATTEMPTS = 5
default_config = {...}    # 应为 DEFAULT_XXX_CONFIG

# ✅
_MAX_ATTEMPTS = 5
DEFAULT_COMPLIANCE_CONFIG = CompliancePromptConfig(...)
```

---

### 2.6 私有符号

| 场景 | 规则 | 示例 |
|------|------|------|
| 模块私有函数 | 单下划线前缀 | `_assert_production_secrets()`、`_check_rate_limit()` |
| 模块私有常量 | 单下划线前缀 | `_MAX_ATTEMPTS`、`_WEAK_SECRET_KEY` |
| 类私有方法 | 单下划线前缀 | `_count_chinese_words()`、`_ensure_minimum_word_count()` |
| 类私有属性 | 单下划线前缀 | `_instance`、`_lock` |
| 双下划线（名称修饰） | **不使用**，除非必须防止子类覆盖 | — |

---

## 3. FastAPI — 路由

### 3.1 URL 路径

**规则：** `kebab-case`，复数名词表资源，动词短语表操作，路径参数 `{snake_case_id}`。

#### 资源 URL 模式

```
GET    /api/v1/{resource}                    # 列表
POST   /api/v1/{resource}                    # 创建
GET    /api/v1/{resource}/{resource_id}      # 单个
PUT    /api/v1/{resource}/{resource_id}      # 更新
DELETE /api/v1/{resource}/{resource_id}      # 删除
```

#### 嵌套资源

```
GET  /api/v1/bases/{base_id}/sources         # 知识库的所有 source
POST /api/v1/bases/{base_id}/sources         # 向知识库添加 source
GET  /api/v1/bases/{base_id}/sources/{source_id}
```

#### 操作型路由（非 CRUD）

```
POST /api/v1/{resource}/{id}/acknowledge     # 动词放在资源之后
POST /api/v1/{resource}/{id}/resolve
POST /api/v1/{resource}/{id}/compress
POST /api/v1/{resource}/{id}/restore
POST /api/v1/chat                            # 动词型资源（聊天本身就是动作）
POST /api/v1/chat/stream
```

#### 导出路由

```
GET /api/v1/{resource}/export/csv
GET /api/v1/{resource}/export/json
```

#### 全部路径词汇表

| 词汇 | 用法 | 对应资源 |
|------|------|----------|
| `conversations` | 复数资源 | 对话列表 |
| `documents` | 复数资源 | 文档列表 |
| `bases` | 复数资源 | 知识库列表 |
| `sources` | 嵌套资源 | 知识库的数据源 |
| `folders` | 复数资源 | 文件夹 |
| `alerts` | 复数资源 | 告警列表 |
| `logs` | 复数资源 | 日志列表 |
| `backups` | 复数资源 | 备份列表 |
| `metrics` | 复数资源 | 指标数据 |
| `health` | 单数（状态词） | 健康检查 |
| `config` | 单数（配置对象） | 配置 |
| `dashboard` | 单数（聚合视图） | 仪表盘 |
| `export/csv` | 子路径 | CSV 导出 |
| `export/json` | 子路径 | JSON 导出 |
| `batch-optimize` | kebab-case 动词短语 | 批量优化操作 |
| `clear-cache` | kebab-case 动词短语 | 清除缓存 |
| `change-password` | kebab-case 动词短语 | 修改密码 |
| `event-types` | kebab-case 复合名词 | 事件类型枚举 |

**禁止：**
```
❌ /api/v1/getDocuments       # 动词出现在 URL 中
❌ /api/v1/document_list      # snake_case 路径
❌ /api/v1/DocumentList       # PascalCase 路径
❌ /api/v1/docs               # 缩写
❌ /api/v1/base/{id}          # 单数资源名（应为 bases）
```

---

### 3.2 路由函数名

**规则：** `snake_case`，遵循 CRUD 动词 + 资源名规范。

| HTTP 方法 | 函数前缀 | 示例 |
|-----------|----------|------|
| `GET`（列表） | `get_{resources}` | `get_documents()`、`get_audit_logs()`、`get_alerts()` |
| `GET`（单个） | `get_{resource}` | `get_document()`、`get_conversation()` |
| `POST` | `create_{resource}` | `create_knowledge_base()`、`create_folder()` |
| `POST`（上传） | `upload_{resource}` | `upload_document()` |
| `POST`（操作） | `{verb}_{resource}` | `acknowledge_alert()`、`batch_optimize_documents()` |
| `PUT` | `update_{resource}` | `update_current_user()` |
| `DELETE` | `delete_{resource}` | `delete_document()`、`delete_knowledge_base()` |
| `WebSocket` | `{resource}_websocket` / `{resource}_websocket_endpoint` | `chat_websocket()`、`audit_websocket_endpoint()` |
| `GET`（导出） | `export_{resource}_{format}` | `export_audit_logs_csv()`、`export_audit_logs_json()` |

---

### 3.3 路由文件名

**规则：** 与资源名对应，`snake_case`，优先用资源名复数。

| 文件名 | 覆盖资源 |
|--------|----------|
| `auth.py` | 认证（login/register/refresh） |
| `chat.py` | 对话与聊天 |
| `documents.py` | 文档管理 |
| `knowledge.py` | 知识库管理 |
| `audit.py` | 审计日志（基础） |
| `audit_enhanced.py` | ❌ 应合并至 `audit.py` |
| `audit_maintenance.py` | 审计维护操作 |
| `audit_websocket.py` | 审计 WebSocket |
| `settings.py` | 系统设置 |
| `monitoring.py` | 监控 |
| `security_enhancement.py` | 安全功能 |
| `security_testing.py` | 安全测试 |

---

## 4. TypeScript/React — 前端

### 4.1 组件文件名

**规则：** `PascalCase`，与组件名一致，后缀 `.tsx`（含 JSX）或 `.ts`（纯逻辑）。

| 模式 | 示例 | 说明 |
|------|------|------|
| 功能名 | `Dashboard.tsx`、`Login.tsx`、`Settings.tsx` | 页面级组件 |
| 功能 + 描述词 | `DocumentPreview.tsx`、`DocumentUpload.tsx` | 功能子组件 |
| 描述词 + 功能 | `FullDocumentPreview.tsx`、`SimpleDocumentPreview.tsx` | 变体组件 |
| 功能 + `Dialog` | `LogDetailDialog.tsx`、`FileUploadDialog.tsx` | 对话框组件 |
| 功能 + `Enhanced` | `AuditLogsEnhanced.tsx` | ❌ 不应使用 `Enhanced`，应版本化 |

**目录结构规则：** 每个组件一个目录，目录名 = 组件名，目录内含 `index.ts` 做统一导出。

```
components/
  DocumentUpload/
    DocumentUpload.tsx    ← 主组件
    DropZone.tsx          ← 子组件
    FileList.tsx
    UploadProgress.tsx
    hooks/
      useFileUpload.ts
    index.ts              ← 统一导出
```

---

### 4.2 组件函数名

**规则：** `PascalCase`，名词或名词短语，与文件名一致。

| 类型 | 示例 |
|------|------|
| 页面组件 | `Dashboard`、`Login`、`Settings`、`KnowledgeBase` |
| 容器组件 | `DocumentDashboard`、`TaskProgressDashboard` |
| UI 原子组件 | `DataCard`、`GradientButton`、`StatusBadge` |
| 对话框 | `LogDetailDialog`、`FileUploadDialog` |
| 布局组件 | `Header`、`MainLayout` |
| 监控组件 | `RealTimeMonitor` |

---

### 4.3 Hook 名

**规则：** `use` + `PascalCase` 动作/资源名，文件名与 Hook 名一致。

| Hook 名 | 文件名 | 职责 |
|---------|--------|------|
| `useFileUpload` | `useFileUpload.ts` | 文件上传逻辑 |
| `useWebSocket` | `useWebSocket.ts` | WebSocket 连接管理 |
| `useReconnect` | `useReconnect.ts` | 自动重连逻辑 |
| `useTheme` | `useTheme.tsx` | 主题切换 |
| `useThemeMode` | （内联） | 主题模式 |
| `useAuth` | （内联） | 认证状态 |
| `useNotification` | （内联） | 通知管理 |
| `useAppDispatch` | `index.ts` | 类型化 dispatch |
| `useAppSelector` | `index.ts` | 类型化 selector |

**命名规则：**
```typescript
// ✅ 正确
useFileUpload()     // 动词 + 资源
useWebSocket()      // 动词 + 资源
useAuth()           // 资源（auth 本身有动作含义）

// ❌ 禁止
useGetDocuments()   // 动词重复（已有 use 前缀）
useDocumentsData()  // 多余的 Data 后缀
useManageFiles()    // manage 过于模糊
```

---

### 4.4 Interface/Type 名

**规则：** `PascalCase`，后缀表职责。

#### 后缀词典

| 后缀 | 场景 | 示例 |
|------|------|------|
| `Props` | React 组件 props | `DataCardProps`、`LogDetailDialogProps`、`DropZoneProps` |
| `State` | Redux state 或 React state | `AuthState`、`ChatState`、`DocumentsState`、`KnowledgeState` |
| `Config` | 配置对象 | `AppConfig`、`FileTypeConfig`、`ModelConfig`、`MessageQueueConfig` |
| `Request` | API 请求体 | `EmbeddingRequest`、`LoginCredentials` |
| `Response` | API 响应体 | `ApiResponse<T>`、`EmbeddingResponse`、`ChatResponse` |
| `ContextType` | React Context 类型 | `AuthContextType`、`NotificationContextType` |
| `ProviderProps` | Context Provider props | `AuthProviderProps`、`NotificationProviderProps` |
| `Result` | 操作结果 | `FileValidationResult`、`ProcessingResult` |
| *(无后缀)* | 领域实体 | `Document`、`Conversation`、`Message`、`KnowledgeBase` |

**禁止：**
```typescript
// ❌
IUser          // 匈牙利记法 I 前缀
TDocumentType  // T 前缀（TypeScript 泛型参数除外）
DocumentData   // Data 后缀无语义

// ✅
User
DocumentType
Document
```

---

### 4.5 Redux Slice 名

**规则：** `camelCase` + `Slice` 后缀（变量名），文件名 `{resource}Slice.ts`（camelCase）。

| 文件名 | Slice 变量名 | State 接口名 |
|--------|-------------|-------------|
| `authSlice.ts` | `authSlice` | `AuthState` |
| `chatSlice.ts` | `chatSlice` | `ChatState` |
| `documentsSlice.ts` | `documentsSlice` | `DocumentsState` |
| `knowledgeSlice.ts` | `knowledgeSlice` | `KnowledgeState` |
| `settingsSlice.ts` | `settingsSlice` | `SettingsState` |
| `uiSlice.ts` | `uiSlice` | `UIState` |

**AsyncThunk 命名：**
```typescript
// 规则：{动词}{资源}（camelCase）
export const fetchDocuments = createAsyncThunk('documents/fetchAll', ...)
export const uploadDocument  = createAsyncThunk('documents/upload', ...)
export const deleteDocument  = createAsyncThunk('documents/delete', ...)
export const loginUser       = createAsyncThunk('auth/login', ...)
```

---

### 4.6 前端变量/函数名

**规则：** `camelCase`，同 Python 动词前缀规律。

```typescript
// 变量
const userId = '...'
const fileSize = 1024
const isLoading = true
const hasError = false

// 函数
const handleSubmit = () => {}
const handleFileSelect = () => {}
const formatFileSize = (bytes: number) => {}
const validateEmail = (email: string) => {}
const fetchDocuments = async () => {}
```

**事件处理函数** 统一以 `handle` 开头：
```typescript
// ✅
onClick={handleSubmit}
onChange={handleFileChange}
onClose={handleDialogClose}

// ❌
onClick={submit}          // 缺少 handle 前缀
onClick={onButtonClick}   // on 前缀仅用于 props 声明
```

---

## 5. 环境变量

**规则：** `SCREAMING_SNAKE_CASE`，前缀表命名空间。

#### 前缀命名空间

| 前缀 | 用途 | 示例 |
|------|------|------|
| `VITE_` | 前端 Vite 构建注入变量 | `VITE_API_BASE_URL`、`VITE_WEBSOCKET_ENABLED` |
| `VITE_FEATURE_` | 前端 Feature Flag | `VITE_FEATURE_STREAMING`、`VITE_FEATURE_FILE_UPLOAD` |
| `LLM_` | LLM 服务配置 | `LLM_PROVIDER`、`LLM_MODEL`、`LLM_TIMEOUT` |
| `EMBEDDING_` | 嵌入服务配置 | `EMBEDDING_PROVIDER`、`EMBEDDING_MODEL`、`EMBEDDING_API_BASE` |
| `RERANKING_` | 重排序服务配置 | `RERANKING_ENABLED`、`RERANKING_MODEL`、`RERANKING_API_BASE` |
| `VECTOR_STORE_` | 向量库配置 | `VECTOR_STORE_TYPE`、`VECTOR_STORE_HOST` |
| `CHROMA_` | ChromaDB 专用配置 | `CHROMA_SERVER_HOST`、`CHROMA_PERSIST_DIRECTORY` |
| `DATABASE_` | 数据库配置 | `DATABASE_URL`、`DATABASE_POOL_SIZE` |
| `REDIS_` | Redis 配置 | `REDIS_URL`、`REDIS_ENABLED` |
| `S3_` | AWS S3 配置 | `S3_BUCKET`、`S3_REGION`、`S3_ACCESS_KEY_ID` |
| `WS_` | WebSocket 配置 | `WS_HEARTBEAT_INTERVAL`、`WS_CONNECTION_TIMEOUT` |
| `ENABLE_` | 功能开关 | `ENABLE_STREAMING`、`ENABLE_AGENT`、`ENABLE_MEMORY` |
| *(无前缀)* | 标准/第三方 Key | `SECRET_KEY`、`DATABASE_URL`、`OPENROUTER_API_KEY`、`NODE_ENV` |

#### 关键变量词典

| 变量名 | 类型 | 说明 |
|--------|------|------|
| `SECRET_KEY` | str | JWT 签名密钥（**生产必须覆盖**） |
| `DATABASE_URL` | str | PostgreSQL 连接串 |
| `REDIS_URL` | str | Redis 连接串 |
| `LLM_PROVIDER` | str | `openai` / `openrouter` / `local` |
| `LLM_BASE_URL` | str | OpenAI 兼容 API 地址 |
| `ENVIRONMENT` | str | `development` / `staging` / `production` |
| `LOG_LEVEL` | str | `DEBUG` / `INFO` / `WARNING` / `ERROR` |

---

## 6. Docker & 容器

### 容器命名

**规则：** `{project}-{service}`，全小写，kebab-case。

| 容器名 | 服务 |
|--------|------|
| `langchain-frontend` | React 前端 |
| `langchain-backend` | FastAPI 主后端 |
| `langchain-embedding` | Embedding Service |
| `langchain-reranking` | Reranking Service |
| `langchain-doc-processor` | 文档处理服务 |
| `langchain-llm-gateway` | LLM 网关 |
| `langchain-postgres` | PostgreSQL |
| `langchain-redis` | Redis |
| `langchain-chromadb` | ChromaDB |
| `langchain-nginx` | Nginx 反向代理 |
| `langchain-prometheus` | Prometheus |
| `langchain-grafana` | Grafana |

> **注意：** 现有容器名前缀为 `langchain-`，生产环境 `docker-compose.prod.yml` 改用 `drass-` 前缀（`drass-main-app`、`drass-vllm` 等）。  
> **规范：** 统一使用项目名 `drass-` 作为前缀，后续新增容器遵循此规则。

### Docker Volume 命名

**规则：** `{service}_{purpose}_data`，全小写，下划线分隔。

| Volume 名 | 用途 |
|-----------|------|
| `postgres_data` | PostgreSQL 持久化数据 |
| `redis_data` | Redis AOF 数据 |
| `chroma_data` | ChromaDB 向量数据 |
| `prometheus_data` | Prometheus 时序数据 |
| `grafana_data` | Grafana 配置数据 |

### 网络命名

**规则：** `{project}-network`，kebab-case。

| 网络名 | 说明 |
|--------|------|
| `langchain-network` | 服务间内部通信网络 |

---

## 7. Shell 脚本

### 脚本文件名

**规则：** `kebab-case`，动词 + 名词（或名词短语）+ `.sh`。

#### 动词前缀词典

| 前缀 | 用途 | 示例 |
|------|------|------|
| `start-` | 启动服务 | `start-system.sh`、`start-frontend-only.sh`、`start-api-noproxy.sh` |
| `stop-` | 停止服务 | `stop-services.sh`、`stop-all.sh` |
| `restart-` | 重启服务 | `restart-ubuntu-services.sh`、`restart-vllm-optimized.sh` |
| `deploy-` | 部署操作 | `deploy.sh`、`deploy-reranking.sh` |
| `build-` | 构建操作 | `build-frontend-prod.sh`、`build-optimized.sh` |
| `check-` | 状态检查 | `check-api.sh`、`check-chromadb.sh`、`check-postgresql.sh` |
| `fix-` | 修复问题 | `fix-dependencies.sh`、`fix-chromadb.sh`、`fix-frontend.sh` |
| `test-` | 测试脚本 | `test-services-health.sh`、`test-all-services.sh` |
| `debug-` | 调试工具 | `debug-port-8000.sh`、`debug-startup.sh` |
| `install-` | 安装依赖 | `install-dependencies.sh`、`install-api-deps.sh` |
| `setup-` | 环境配置 | `setup-venv.sh` |
| `cleanup-` / `clean-` | 清理 | `cleanup-stale.sh`、`clean-vectorstore.sh` |
| `configure-` / `configure_` | 配置 | `configure_production.sh` |

> **不一致问题：** 现有脚本混用 `kebab-case`（`start-system.sh`）和 `snake_case`（`install_deps.sh`、`quick_test.sh`、`configure_production.sh`）。  
> **规范：** 统一使用 `kebab-case`。

### Shell 脚本内部函数名

**规则：** `snake_case`，动词 + 名词，与 Python 函数命名一致。

```bash
# ✅ 当前使用的正确模式
start_infrastructure()
start_microservices()
start_llm()
start_backend()
start_frontend()
cleanup_existing()
setup_environment()
wait_for_service()
wait_for_tcp()        # 新增的就绪探针函数
check_port()
kill_port()
print_status()
print_success()
print_error()
print_warning()
print_section()
test_system()
show_status()
```

### Shell 变量名

**规则：** 全局配置变量用 `SCREAMING_SNAKE_CASE`，局部变量用 `snake_case`。

```bash
# 全局配置（SCREAMING_SNAKE_CASE）
PROJECT_ROOT="..."
DOCKER_COMPOSE_FILE="docker-compose.yml"
LOG_DIR="$PROJECT_ROOT/logs"
PID_DIR="$PROJECT_ROOT/.pids"
RED='\033[0;31m'

# 局部变量（snake_case）
local port=$1
local elapsed=0
local max_attempts=30
```

---

## 8. 日志文件

**规则：** `{service}.log`，全小写，kebab-case 服务名，放在 `logs/` 目录。

| 日志文件 | 对应服务 |
|----------|----------|
| `logs/backend.log` | FastAPI 主后端 |
| `logs/frontend.log` | React 前端 dev server |
| `logs/llm.log` | 本地 LLM 服务 |
| `logs/embedding.log` | Embedding Service |
| `logs/reranking/` | Reranking Service（目录） |

---

## 9. 数据库/模型

### Pydantic ORM 模型

**规则：** 类名遵循 2.2 节规范；字段名 `snake_case`。

```python
class AuditLogDB(Base):
    __tablename__ = "audit_logs"   # 表名：snake_case 复数
    
    id: int                        # 主键：id
    user_id: str                   # 外键：{entity}_id
    event_type: str                # 枚举字段：snake_case
    created_at: datetime           # 时间戳：{action}_at
    updated_at: datetime
    is_active: bool                # 布尔字段：is_ 前缀
```

### 数据库表名规则

| 规则 | 示例 |
|------|------|
| `snake_case` 复数名词 | `audit_logs`、`audit_log_archives` |
| 关联表（多对多） | `{entity_a}_{entity_b}s` |
| 不使用 `tbl_` 前缀 | ❌ `tbl_audit_logs` |

---

## 10. 不一致问题清单

以下为当前代码库中发现的命名不一致问题，应在后续迭代中修正：

| 问题 | 现状 | 规范建议 | 优先级 |
|------|------|----------|--------|
| Python 服务文件 `_enhanced` 后缀 | `audit_service_enhanced.py`、`llm_service_enhanced.py` | 功能合并或用版本号区分 | HIGH |
| Python 服务文件 `_optimized` 后缀 | `vector_store_optimized.py` | 删除旧版或重命名 | HIGH |
| React 组件 `Enhanced` 后缀 | `AuditLogsEnhanced.tsx` | 同上，功能合并 | HIGH |
| Shell 脚本混用分隔符 | `install_deps.sh`（snake）vs `start-system.sh`（kebab） | 统一 kebab-case | MEDIUM |
| 容器名前缀不统一 | `langchain-*`（开发）vs `drass-*`（生产） | 统一改为 `drass-*` | MEDIUM |
| 中文脚本文件名 | `强制清理缓存.sh` | 改为 `force-clear-cache.sh` | HIGH |
| 路由函数名无法体现 HTTP 方法 | `audit_logs()` 不清楚是 GET/POST | 改为 `get_audit_logs()` | MEDIUM |
| `test_` 前缀的生产代码类 | `TestChatRequest`、`TestDocumentRequest` | 仅测试文件中使用 `Test` 前缀 | HIGH |
| `_service` 后缀不一致 | `vector_store.py` 无后缀 vs `chat_service.py` 有后缀 | 统一加 `_service` 后缀 | MEDIUM |

---

## 11. 快速参考卡

```
╔══════════════════════════════════════════════════════════════════════╗
║                    DRASS 命名规范速查表                              ║
╠══════════════════════════════════════╦═══════════════════════════════╣
║ 场景                                 ║ 规则                          ║
╠══════════════════════════════════════╬═══════════════════════════════╣
║ Python 模块/文件名                   ║ snake_case.py                 ║
║ Python 类名                          ║ PascalCase + 职责后缀         ║
║ Python 函数/方法名                   ║ snake_case，动词开头           ║
║ Python 变量名                        ║ snake_case，名词               ║
║ Python 常量名                        ║ SCREAMING_SNAKE_CASE          ║
║ Python 私有符号                      ║ _single_underscore 前缀       ║
╠══════════════════════════════════════╬═══════════════════════════════╣
║ FastAPI URL 路径                     ║ /api/v1/kebab-case/{id}       ║
║ FastAPI 路由函数名                   ║ get/create/update/delete_资源  ║
║ FastAPI 路由文件名                   ║ resource_name.py              ║
╠══════════════════════════════════════╬═══════════════════════════════╣
║ TS/React 组件文件名                  ║ PascalCase.tsx                ║
║ TS/React 组件名                      ║ PascalCase                    ║
║ TS/React Hook 名                     ║ usePascalCase                 ║
║ TS Interface/Type 名                 ║ PascalCase + 职责后缀         ║
║ TS Redux Slice 文件名                ║ camelCaseSlice.ts             ║
║ TS 变量/函数名                       ║ camelCase                     ║
║ TS 事件处理器                        ║ handlePascalCase              ║
╠══════════════════════════════════════╬═══════════════════════════════╣
║ 环境变量                             ║ SCREAMING_SNAKE_CASE          ║
║ 前端环境变量                         ║ VITE_SCREAMING_SNAKE_CASE     ║
╠══════════════════════════════════════╬═══════════════════════════════╣
║ Docker 容器名                        ║ drass-kebab-case              ║
║ Docker Volume 名                     ║ service_purpose_data          ║
║ Docker 网络名                        ║ drass-network                 ║
╠══════════════════════════════════════╬═══════════════════════════════╣
║ Shell 脚本文件名                     ║ verb-noun.sh（kebab-case）    ║
║ Shell 内部函数名                     ║ snake_case                    ║
║ Shell 全局变量                       ║ SCREAMING_SNAKE_CASE          ║
║ Shell 局部变量                       ║ snake_case                    ║
╠══════════════════════════════════════╬═══════════════════════════════╣
║ 数据库表名                           ║ snake_case_plural             ║
║ 数据库字段名                         ║ snake_case                    ║
║ 日志文件名                           ║ service-name.log              ║
╚══════════════════════════════════════╩═══════════════════════════════╝

动词前缀规律（Python & TS 通用）：
  get_     查询      create_  创建      update_  更新
  delete_  删除      upload_  上传      export_  导出
  check_   验证      verify_  验证凭据  validate_ 格式校验
  build_   构建      generate_ 生成     init_    初始化
  cleanup_ 清理      handle_  处理事件  process_ 处理数据
  is_/has_/can_ 布尔函数前缀

职责后缀规律（类名）：
  Python:     Service  Manager  Factory  Chain  Tool  Handler  Agent
  TypeScript: Props    State    Config   Request Response  ContextType
```
