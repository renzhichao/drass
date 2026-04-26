# LangChain 合规助手实现说明

> 状态：已从“宏观技术方案”收敛为“当前实现概览”。

这份文档不再描述一个过于理想化、覆盖 AWS 分布式与多网关的总方案，而是聚焦当前仓库里已经存在的实现骨架。

## 当前项目事实

Drass 目前的主链路是一个多服务系统：

```text
Frontend
  -> Main API
     -> LLM
     -> Embedding
     -> Reranking
     -> ChromaDB
     -> Redis / PostgreSQL
```

## LangChain 相关代码位置

当前 LangChain 相关实现主要集中在：

- `services/main-app/app/chains/`
- `services/main-app/app/services/`
- `services/main-app/app/agents/`

其中：

- `chains/` 负责 RAG 与提示链逻辑
- `services/` 负责模型、向量、文档、缓存、监控等能力封装
- `agents/` 负责工具化与代理式交互扩展

## 当前前端与后端关系

前端不再只是单一聊天壳层，而是包含：

- 登录
- 仪表盘
- 文档上传
- 文档浏览
- 审计日志
- 知识库
- 设置
- 简化聊天界面

后端承担：

- API 中枢
- 文档流程编排
- RAG 调用编排
- 审计与监控接口

## 当前更准确的架构理解

### 应用层

- `frontend/`
- `services/main-app/`

### AI 能力层

- `qwen3_api_server.py` 或其他 OpenAI 兼容 LLM
- `services/embedding-service/`
- `services/reranking-service/`

### 数据层

- ChromaDB
- Redis
- PostgreSQL
- 本地上传目录

## 当前实现与历史方案之间的主要差异

过去文档的问题主要是：

1. 把 AWS / ECS / EKS 级别方案写成当前既成事实
2. 把大量“应有组件”写成“已有组件”
3. 把技术栈设计与真实目录、端口、脚本脱节

当前更准确的说法是：

1. 项目已经具备多服务骨架
2. 但部署路径、变量名、接口契约仍在收敛
3. 应以当前仓库代码和启动脚本为准，而不是以旧技术蓝图为准

## 当前最值得看的相关文档

- `README.md`
- `README_LANGCHAIN.md`
- `docs/chensha_运行依赖分析.md`
- `docs/ONE_CLICK_STARTUP_GUIDE.md`

## 本文档已去掉的失效内容

本次去掉了：

1. 大量未在当前仓库中形成闭环的云原生总架构描述
2. 把若干未来态服务当成当前已落地实现的写法
3. 与当前代码目录不完全一致的分层设计图
4. 大段脱离当前仓库状态的示例代码
