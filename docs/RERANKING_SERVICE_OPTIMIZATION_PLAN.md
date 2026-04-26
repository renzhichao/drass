# Reranking 服务优化说明

> 状态：历史优化方案，非当前现状文档。

这份文档记录的是某一轮针对 `reranking-service` 的诊断与优化计划。它不再适合作为当前系统事实说明，因为其中包含：

1. 阶段性的“当前问题分析”
2. 当时的目标架构
3. 中间态端口与前端入口示例
4. 计划型实现细节

## 当前为什么需要降级

在本轮复查中，这份文档仍保留了旧入口示例，例如：

- `http://localhost:3000`

而当前项目主文档已经不再把该端口作为主入口基线。

## 当前更准确的参考方式

如果要看 `reranking-service` 的当前角色，应优先参考：

- `services/reranking-service/README.md`
- `services/reranking-service/MIGRATION_GUIDE.md`
- `README.md`
- `docs/chensha_运行依赖分析.md`

## 当前建议

1. 把本文档视为历史优化思路记录。
2. 不再从中提取当前端口、入口、流程作为事实。
3. 若后续继续维护该服务，建议补一份“当前实现说明”，而不是继续沿用历史优化方案文档。
