# Drass 项目依赖关系图

> 生成日期：2026-04-26

---

## 架构总览

```
浏览器
  ├── Nginx（可选反向代理）
  │     ├── 前端 Frontend :5173
  │     └── 主后端 main-app :8000
  └── 直连（开发模式）
        ├── 前端 Frontend :5173
        └── 主后端 main-app :8000
```

---

## 服务依赖关系

### 服务间依赖

```
前端 :5173
  └──HTTP/WebSocket──► 主后端 main-app :8000
                           ├── Embedding Service :8002
                           ├── Reranking Service :8004
                           ├── Doc Processor :5003
                           ├── LLM Gateway :8003（可选）
                           ├── PostgreSQL :5432
                           ├── Redis :6379
                           └── ChromaDB :8005

Embedding Service :8002
  └── Redis :6379（缓存）

Reranking Service :8004
  └── Redis :6379（缓存）

LLM Gateway :8003
  ├── 本地 Qwen3-8B-MLX :8001
  └── OpenRouter API（云端）

主后端 LangChain
  ├── 本地 Qwen3-8B-MLX :8001
  └── OpenRouter API（云端）

Scheduler Service
  └──HTTP──► 主后端 main-app :8000

Prometheus :9090（可选监控）
  └── Grafana :3001
```

---

## 各服务依赖明细

### 🖥️ 前端 Frontend（:5173）

| 包名 | 版本 | 用途 |
|------|------|------|
| react | ^18.2.0 | 核心 UI 框架 |
| react-dom | ^18.2.0 | DOM 渲染 |
| typescript | ^5.3.3 | 类型系统 |
| vite | ^5.0.10 | 构建工具 |
| @mui/material | ^5.15.0 | UI 组件库 |
| @mui/icons-material | ^5.15.0 | 图标库 |
| @emotion/react | ^11.11.1 | CSS-in-JS（MUI 依赖） |
| @emotion/styled | ^11.11.0 | CSS-in-JS（MUI 依赖） |
| @reduxjs/toolkit | ^2.0.1 | 状态管理 |
| react-redux | ^9.0.4 | Redux React 绑定 |
| react-query | ^3.39.3 | 服务端状态管理 |
| react-router-dom | ^6.20.1 | 路由 |
| axios | ^1.11.0 | HTTP 客户端 |
| socket.io-client | ^4.5.4 | WebSocket 实时通信 |
| react-hook-form | ^7.48.2 | 表单管理 |
| react-markdown | ^9.1.0 | Markdown 渲染 |
| rehype-highlight | ^7.0.2 | 代码高亮 |
| rehype-katex | ^7.0.1 | 数学公式渲染 |
| remark-gfm | ^4.0.1 | GitHub Flavored Markdown |
| remark-math | ^6.0.0 | 数学语法支持 |
| react-syntax-highlighter | ^15.5.0 | 代码语法高亮 |
| react-dropzone | ^14.3.8 | 文件拖拽上传 |
| react-pdf | ^10.1.0 | PDF 预览 |
| i18next | ^25.5.2 | 国际化框架 |
| react-i18next | ^15.7.3 | i18n React 绑定 |
| date-fns | ^3.6.0 | 日期处理 |
| lodash | ^4.17.21 | 工具函数库 |
| uuid | ^9.0.1 | UUID 生成 |

**开发依赖：**

| 包名 | 版本 | 用途 |
|------|------|------|
| vitest | ^1.1.0 | 单元测试框架 |
| @testing-library/react | ^14.1.2 | React 组件测试 |
| @testing-library/jest-dom | ^6.1.5 | DOM 断言 |
| @testing-library/user-event | ^14.5.1 | 用户事件模拟 |
| eslint | ^8.56.0 | 代码检查 |
| prettier | ^3.1.1 | 代码格式化 |
| jsdom | ^23.0.1 | 测试 DOM 环境 |

---

### ⚙️ 主后端 main-app（:8000）

| 包名 | 版本 | 用途 |
|------|------|------|
| fastapi | 0.109.0 | Web 框架 |
| uvicorn[standard] | 0.27.0 | ASGI 服务器 |
| python-multipart | 0.0.6 | 文件上传支持 |
| pydantic | 2.5.3 | 数据验证 |
| pydantic-settings | 2.1.0 | 配置管理 |
| email-validator | 2.1.0 | 邮箱验证 |
| python-jose[cryptography] | 3.3.0 | JWT 认证 |
| passlib[bcrypt] | 1.7.4 | 密码哈希 |
| bcrypt | 4.1.2 | 加密算法 |
| langchain | 0.1.0 | LLM 编排框架 |
| langchain-community | 0.0.10 | 社区扩展 |
| langchain-openai | 0.0.2 | OpenAI 集成 |
| openai | 1.6.1 | OpenAI SDK |
| tiktoken | 0.5.2 | Token 计数 |
| chromadb | 0.4.22 | 向量数据库客户端 |
| cohere | 4.39.0 | Cohere Reranking |
| sentence-transformers | >=5.1.0 | 本地 Embedding |
| pypdf | 3.17.4 | PDF 解析 |
| python-docx | 1.1.0 | Word 文档解析 |
| openpyxl | 3.1.2 | Excel 解析 |
| python-pptx | 0.6.23 | PPT 解析 |
| pytesseract | 0.3.10 | OCR 文字识别 |
| Pillow | 10.2.0 | 图像处理 |
| markdown | 3.5.1 | Markdown 解析 |
| beautifulsoup4 | 4.12.2 | HTML 解析 |
| chardet | 5.2.0 | 编码检测 |
| redis | 5.0.1 | Redis 缓存客户端 |
| httpx | 0.26.0 | 异步 HTTP 客户端 |
| aiohttp | 3.9.1 | 异步 HTTP 框架 |
| python-dotenv | 1.0.0 | 环境变量加载 |
| pyyaml | 6.0.1 | YAML 解析 |
| orjson | 3.9.10 | 高性能 JSON |
| prometheus-client | 0.19.0 | Prometheus 指标采集 |
| structlog | 24.1.0 | 结构化日志 |
| slowapi | 0.1.9 | API 限速 |
| cachetools | 5.3.2 | 内存缓存工具 |
| boto3 | 1.34.14 | AWS S3 存储 |
| pytest | 7.4.4 | 测试框架 |
| pytest-asyncio | 0.23.3 | 异步测试支持 |
| pytest-cov | 4.1.0 | 覆盖率报告 |

---

### 🔢 Embedding Service（:8002）

| 包名 | 版本 | 用途 |
|------|------|------|
| fastapi | 0.109.0 | Web 框架 |
| uvicorn[standard] | 0.27.0 | ASGI 服务器 |
| pydantic | 2.5.3 | 数据验证 |
| sentence-transformers | 2.2.2 | 本地向量化模型 |
| torch | >=2.0.0 | 深度学习框架 |
| openai | 1.6.1 | OpenAI Embedding（可选） |
| cohere | 4.39.0 | Cohere Embedding（可选） |
| numpy | 1.24.3 | 数值计算 |
| redis | 5.0.1 | 向量缓存 |
| httpx | 0.25.2 | HTTP 客户端 |
| tenacity | 8.2.3 | 重试逻辑 |
| python-dotenv | 1.0.0 | 环境变量 |

---

### 🔀 Reranking Service（:8004）

| 包名 | 版本 | 用途 |
|------|------|------|
| fastapi | 0.104.1 | Web 框架 |
| uvicorn[standard] | 0.24.0 | ASGI 服务器 |
| pydantic | 2.5.0 | 数据验证 |
| pydantic-settings | 2.1.0 | 配置管理 |
| sentence-transformers | 2.7.0 | Cross-Encoder 重排模型 |
| torch | >=2.0.0 | 深度学习框架 |
| numpy | >=1.24.0 | 数值计算 |
| scikit-learn | >=1.3.0 | 机器学习工具 |
| redis[hiredis] | 5.0.1 | 结果缓存（含 hiredis 加速） |
| aioredis | 2.0.1 | 异步 Redis |
| huggingface_hub | >=0.20.0 | 模型下载管理 |
| prometheus-client | 0.19.0 | 指标采集 |
| structlog | 24.1.0 | 结构化日志 |
| python-jose[cryptography] | 3.3.0 | JWT 验证 |
| passlib[bcrypt] | 1.7.4 | 密码处理 |
| httpx | 0.25.2 | HTTP 客户端 |
| python-multipart | 0.0.6 | 文件上传 |
| pytest | 7.4.3 | 测试框架 |
| pytest-asyncio | 0.21.1 | 异步测试 |
| pytest-cov | 4.1.0 | 覆盖率 |

---

### 📄 Doc Processor（:5003）

| 包名 | 版本 | 用途 |
|------|------|------|
| Flask | 2.3.3 | Web 框架 |
| flask-cors | 4.0.0 | 跨域支持 |
| python-docx | 0.8.11 | Word 文档处理 |
| PyPDF2 | 3.0.1 | PDF 解析 |
| openpyxl | 3.1.2 | Excel 处理 |
| python-pptx | 0.6.21 | PPT 处理 |
| markdown | 3.4.4 | Markdown 解析 |
| beautifulsoup4 | 4.12.2 | HTML 解析 |
| pytesseract | 0.3.10 | OCR（中英文） |
| Pillow | 10.0.0 | 图像处理 |
| python-magic | 0.4.27 | 文件类型检测 |
| chardet | 5.2.0 | 编码检测 |
| numpy | 1.24.3 | 语义分割数值计算 |
| scikit-learn | 1.3.0 | 语义分割算法 |
| pyyaml | 6.0.1 | YAML 配置 |
| requests | 2.31.0 | HTTP 请求 |
| python-dotenv | 1.0.0 | 环境变量 |

---

### 🔀 LLM Gateway（:8003）

| 包名 | 版本 | 用途 |
|------|------|------|
| fastapi | 0.104.1 | Web 框架 |
| uvicorn[standard] | 0.24.0 | ASGI 服务器 |
| httpx | 0.25.1 | 异步 HTTP 代理转发 |
| pydantic | 2.5.0 | 数据验证 |
| pydantic-settings | 2.1.0 | 配置管理 |
| pyyaml | 6.0.1 | Provider 配置解析 |
| redis | 5.0.1 | 响应缓存 |
| cachetools | 5.3.2 | 内存缓存 |
| prometheus-client | 0.19.0 | 指标采集 |
| aiofiles | 23.2.1 | 异步文件读写 |
| python-multipart | 0.0.6 | 表单解析 |
| python-dotenv | 1.0.0 | 环境变量 |

---

### ⏱️ Scheduler Service

| 包名 | 版本 | 用途 |
|------|------|------|
| apscheduler | 3.10.4 | 任务调度框架 |
| requests | 2.31.0 | HTTP 调用后端 API |
| loguru | 0.7.2 | 日志记录 |
| python-dotenv | 1.0.0 | 环境变量 |
| python-dateutil | 2.8.2 | 时间处理 |
| pyyaml | 6.0.1 | 调度配置 |

---

### 🗄️ 数据层（基础设施镜像）

| 服务 | 镜像 | 端口 | 用途 |
|------|------|------|------|
| PostgreSQL | postgres:15-alpine | :5432 | 关系型数据库 |
| Redis | redis:7-alpine | :6379 | 缓存 / 消息队列 |
| ChromaDB | chromadb/chroma:latest | :8005 | 向量数据库 |

---

### 📊 监控层（可选，`--profile monitoring`）

| 服务 | 镜像 | 端口 | 用途 |
|------|------|------|------|
| Prometheus | prom/prometheus:latest | :9090 | 指标收集 |
| Grafana | grafana/grafana:latest | :3001 | 可视化仪表盘 |

---

### 🤖 外部 LLM 服务

| 服务 | 地址 | 用途 |
|------|------|------|
| 本地 Qwen3-8B-MLX | http://localhost:8001/v1 | Apple Silicon 本地推理（MLX） |
| OpenRouter API | https://openrouter.ai/api/v1 | 云端多模型路由 |

---

## 端口映射总览

| 服务 | 容器端口 | 宿主机端口 |
|------|----------|------------|
| Frontend | 5173 | 5173 |
| main-app | 8000 | 8000 |
| Embedding Service | 8001 | 8002 |
| Reranking Service | 8002 | 8004 |
| Doc Processor | 5003 | 5003 |
| LLM Gateway | 8003 | 8003 |
| PostgreSQL | 5432 | 5432 |
| Redis | 6379 | 6379 |
| ChromaDB | 8000 | 8005 |
| Prometheus | 9090 | 9090 |
| Grafana | 3000 | 3001 |
| Nginx | 80/443 | 80/443 |
| 本地 LLM（宿主机） | — | 8001 |

---

## 共享依赖说明

以下包被多个服务共同依赖：

- **`redis`** — main-app、embedding-service、reranking-service、llm-gateway 均使用 Redis 做缓存
- **`fastapi + uvicorn`** — main-app、embedding-service、reranking-service、llm-gateway 均基于 FastAPI 构建
- **`pydantic`** — 所有 Python 服务均使用 Pydantic 做数据验证
- **`sentence-transformers + torch`** — embedding-service 和 reranking-service 共享
- **`prometheus-client`** — main-app、reranking-service、llm-gateway 均暴露 `/metrics`
- **`python-dotenv + pyyaml`** — 全部 Python 服务共用
- **`httpx`** — main-app、embedding-service、reranking-service、llm-gateway 均使用

---

## FigJam 可视化

图表已同步至 FigJam：[Drass 项目依赖关系图](https://www.figma.com/board/jTbjrA2SSmOBNA8Lp1hYKS?utm_source=claude_code&utm_content=edit_in_figjam)
