# Reranking 服务任务清单说明

> 状态：阶段性任务单，非当前主文档。

这份文档原先是某一轮 `reranking-service` 重构的任务列表。它属于项目过程记录，不应再作为当前系统说明文档使用。

## 为什么降级

1. 任务状态、日期、优先级都强依赖特定时间点
2. 文档中的“已完成/待完成”很容易与当前代码状态脱节
3. 它更适合做历史追踪，不适合继续放在主文档链路里

## 当前建议

如果要确认 `reranking-service` 的现状，请优先看：

- `services/reranking-service/README.md`
- `services/reranking-service/MIGRATION_GUIDE.md`
- `docs/chensha_运行依赖分析.md`

如果要继续做重构管理，应单独使用任务系统或 issue，而不是依赖这类长期滞留的 Markdown 任务单。
