# 系统提示词集成说明

> 状态：历史方案说明，不作为当前主实现文档。

这份文档原本记录的是一轮“把旧 Dify 提示词迁移到 LangChain 系统”的实现计划。它属于阶段性方案文档，不适合继续作为当前系统事实说明。

## 为什么降级

主要原因：

1. 文档强依赖旧 Dify 语境
2. 文档是计划稿，不是现状文档
3. 它容易让人误以为当前提示词机制仍然以该迁移方案为主线

## 当前更准确的理解

当前如果要看提示词相关实现，应直接看代码：

- `services/main-app/app/chains/prompts.py`
- `services/main-app/app/chains/compliance_prompts.py`
- `services/main-app/app/chains/compliance_rag_chain.py`

## 建议

后续应把“计划稿”和“已实现说明”彻底分开管理。本文档保留为历史背景，不再作为主入口。
