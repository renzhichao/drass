# Drass

Drass 当前是一个多服务的数据合规分析与 RAG 辅助系统，不再是最初的 Dify 配置工程。仓库内同时包含前端、主后端、文档处理、向量检索、重排、部署脚本和生产化配置。

## 当前项目定位

- `frontend/`：React + Vite 前端
- `services/main-app/`：FastAPI 主后端
- `services/doc-processor/`：文档转换与 OCR
- `services/embedding-service/`：嵌入服务
- `services/reranking-service/`：重排服务
- `deployment/`、`production/`：部署、systemd、Nginx、监控、备份相关配置

## 运行架构

```text
Browser
  -> Frontend (5173)
  -> Main API (开发常见 8000 / 生产基线 8888)
     -> LLM Service (8001)
     -> Embedding Service (常见 8002 或 8010，取决于部署模式)
     -> Reranking Service (常见 8004 或 8012，取决于部署模式)
     -> ChromaDB (8005)
     -> Redis (6379)
     -> PostgreSQL (5432，可选但推荐正式接入)
```

## 推荐阅读顺序

- 项目入口：`README.md`
- 启动说明：[docs/ONE_CLICK_STARTUP_GUIDE.md](docs/ONE_CLICK_STARTUP_GUIDE.md)
- 运行依赖分析：[docs/chensha_运行依赖分析.md](docs/chensha_运行依赖分析.md)
- 部署与基础设施规则：[docs/chensha_部署与基础设施规则.md](docs/chensha_部署与基础设施规则.md)
- 文档清理与校正说明：`docs/文档清理与校正说明.md`

## 当前推荐启动方式

### 1. 本地综合联调

优先看 `start-system.sh`，它尝试按“本地 LLM + 本地后端 + 本地前端 + Docker 基础设施”方式启动系统。

```bash
./start-system.sh
```

适合：

- 本地功能验证
- 前后端联调
- RAG 链路排查

### 2. 分开启动 API 与前端

如果你只想单独验证服务，可使用：

```bash
./start-api-noproxy.sh
./start-frontend-only.sh
```

适合：

- Ubuntu/远程主机排障
- API 单独验证
- 前端页面联调

### 3. Ubuntu AMD GPU 部署路径

如果是已有独立 LLM / Embedding / Reranking 服务的 Ubuntu 环境，优先看：

```bash
deployment/scripts/start-ubuntu-services.sh
```

## 需要特别注意的现状

当前仓库存在历史文档与配置漂移，使用前应知道：

1. 有些旧文档仍把项目描述为 Dify 配置工程，这已经不准确。
2. 开发链路和生产链路使用过两套主端口：
   - 开发常见：`8000`
   - 生产基线：`8888`
3. 部分文档仍引用已不存在或不再推荐的脚本名。
4. AI 服务和后端之间的变量命名、端口和接口协议仍在收敛中。

因此，当前应以这几个文件为准：

- `README.md`
- `docs/ONE_CLICK_STARTUP_GUIDE.md`
- `docs/chensha_运行依赖分析.md`
- `docs/chensha_部署与基础设施规则.md`
- `docs/文档清理与校正说明.md`

## 文档治理说明

这次仓库整理的目标不是“补更多文档”，而是先纠正文档事实：

- 去掉已经失效的启动入口描述
- 去掉与当前项目不符的 Dify 主叙事
- 把真正的服务结构、端口基线和部署入口收拢出来

如果你后续继续整理，建议优先做两件事：

1. 继续归档历史说明文档，减少重复入口。
2. 统一开发态与生产态的端口、变量名和服务契约。
