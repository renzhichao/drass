# 启动指南

本文档只保留当前仓库里仍然存在、且相对可用的启动入口。旧文档中提到的 `start-simple.sh`、`start-langchain.sh`、`start-full-langchain.sh` 不再作为当前项目入口使用。

## 启动模式

### 模式一：本地综合联调

脚本：

```bash
./start-system.sh
```

用途：

- 本地完整链路调试
- 尝试拉起前端、主后端、本地 LLM，以及部分 Docker 基础设施

典型端口：

- Frontend：`5173`
- Main API：`8000`
- LLM：`8001`
- Embedding：`8002`
- Reranking：`8004`
- Doc Processor：`5003`
- ChromaDB：`8005`
- PostgreSQL：`5432`
- Redis：`6379`

说明：

1. 这是当前仓库里最接近“开发态一键启动”的入口。
2. 脚本会尝试创建 `.env`、清理端口、拉起 Docker 基础设施、再启动应用层服务。
3. 由于仓库仍存在配置漂移，这个脚本适合调试，不应直接视为生产启动方案。

### 模式二：分开启动 API 与前端

脚本：

```bash
./start-api-noproxy.sh
./start-frontend-only.sh
```

用途：

- 在已有独立 AI 服务的机器上单独启动应用层
- 排查代理、端口、环境变量问题
- 分离前后端调试

典型端口：

- Frontend：`5173`
- Main API：`8888`
- LLM：`8001`
- Embedding：`8010`
- Reranking：`8012`

说明：

1. 这组脚本更接近 Ubuntu/生产风格的服务布局。
2. `start-api-noproxy.sh` 会主动清理代理变量，并显式注入 LLM、Embedding、Reranking 地址。
3. 如果你的目标是远程主机排障，这一组通常比 `start-system.sh` 更直接。

### 模式三：Ubuntu AMD GPU 生产风格启动

脚本：

```bash
deployment/scripts/start-ubuntu-services.sh
```

用途：

- Ubuntu 22.04 主机
- 已有或计划接入独立 LLM / Embedding / Reranking 服务
- 接近生产的本机服务化运行方式

典型端口：

- Frontend：`5173`
- Main API：`8888`
- ChromaDB：`8005`
- PostgreSQL：`5432`
- Redis：`6379`
- LLM：`8001`
- Embedding：`8010`
- Reranking：`8012`

说明：

1. 这是当前仓库里最明确的“生产风格”启动入口。
2. 更完整的生产约束见 `production/`、`deployment/` 和 `docs/chensha_部署与基础设施规则.md`。

## 停止方式

### 开发态停止

```bash
./stop-services.sh
```

适用：

- `start-system.sh` 拉起的本地服务

### Ubuntu 服务停止

```bash
deployment/scripts/stop-ubuntu-services.sh
```

适用：

- Ubuntu 主机上的 API、前端、ChromaDB、Redis 等服务清理

## 当前推荐顺序

如果你是第一次接手这个项目，建议按下面顺序：

1. 先看 `README.md`
2. 再看 `docs/chensha_运行依赖分析.md`
3. 然后根据目标环境选择启动模式

建议选择：

- 本地开发：`./start-system.sh`
- 远程 Ubuntu / 已有 AI 服务：`./start-api-noproxy.sh` + `./start-frontend-only.sh`
- 接近生产部署：`deployment/scripts/start-ubuntu-services.sh`

## 已失效或不再推荐的入口

以下内容在旧文档里出现过，但不应再作为当前入口：

- `./start-simple.sh`
- `./start-langchain.sh`
- `./start-full-langchain.sh`
- 以 `3000` / `8080` 为当前主链路默认端口的说明
- 仍把项目描述为“仅 Dify 配置工程”的启动说明

## 已知注意事项

1. 开发态和生产态目前存在两套主后端端口：
   - 开发常见：`8000`
   - 生产基线：`8888`
2. `frontend`、`main-app`、AI 服务之间仍有部分变量命名和协议待收敛。
3. 根目录 `docker-compose.yml` 可用于理解整体架构，但不代表所有服务都能零修正直接构建。

## 相关文档

- [README](../README.md)
- [运行依赖分析](./chensha_运行依赖分析.md)
- [部署与基础设施规则](./chensha_部署与基础设施规则.md)
- `docs/文档清理与校正说明.md`
