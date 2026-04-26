# LangChain 架构说明

这份文档保留为架构补充说明，不再承担项目主入口职责。项目当前的权威入口是 [README.md](README.md)。

## 当前定位

Drass 的核心业务链路是：

```text
Frontend
  -> Main API
     -> LLM Provider
     -> Embedding Service
     -> Reranking Service
     -> ChromaDB
     -> Redis / PostgreSQL
```

`LangChain` 主要集中在：

- `services/main-app/app/chains/`
- `services/main-app/app/services/`
- `services/main-app/app/agents/`

## 当前服务基线

开发态常见：

- Frontend：`5173`
- Main API：`8000`
- LLM：`8001`
- Embedding：`8002`
- Reranking：`8004`
- ChromaDB：`8005`

生产风格常见：

- Frontend：`5173`
- Main API：`8888`
- LLM：`8001`
- Embedding：`8010`
- Reranking：`8012`
- ChromaDB：`8005`

## 需要注意的现实情况

1. 这个仓库保留了多轮迭代痕迹，所以开发端口和生产端口不完全一致。
2. 部分历史文档仍引用旧脚本或旧接口，不应直接照抄。
3. 当前应优先参考：
   - `README.md`
   - `docs/ONE_CLICK_STARTUP_GUIDE.md`
   - `docs/chensha_运行依赖分析.md`

## 启动建议

本地联调：

```bash
./start-system.sh
```

Ubuntu / 已有 AI 服务：

```bash
./start-api-noproxy.sh
./start-frontend-only.sh
```

生产风格部署：

```bash
deployment/scripts/start-ubuntu-services.sh
```

## 这份文档不再包含的内容

以下历史内容已从本文件移除：

- 不存在的 `start-full-langchain.sh`
- 已失效的 `start-simple.sh` 启动路径
- 把全部接口和端口固定写成单一旧值的说明
- 与当前项目结构不符的全量功能承诺
