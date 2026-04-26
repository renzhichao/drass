# services 目录说明

本目录存放 Drass 的服务实现。当前应把这里理解为“业务服务与基础能力服务集合”，而不是单一的微服务样例目录。

## 当前目录

| 目录 | 作用 | 现状 |
| --- | --- | --- |
| `main-app/` | 主后端 API、RAG、审计、文档、配置 | 核心服务 |
| `doc-processor/` | 文档转换、OCR、切分 | 可独立运行 |
| `embedding-service/` | 文本嵌入服务 | 可独立运行 |
| `reranking-service/` | 检索重排服务 | 可独立运行 |
| `llm-gateway/` | 多模型网关 | 可选增强 |
| `scheduler/` | 定时任务样例/辅助服务 | 非当前主链路 |
| `data/` | 服务相关数据目录 | 持久化内容 |

## 核心关系

```text
main-app
  -> doc-processor
  -> embedding-service
  -> reranking-service
  -> ChromaDB
  -> Redis
  -> PostgreSQL
```

## 当前更准确的服务说明

### 1. `main-app`

职责：

- 提供主 API
- 协调 LLM、Embedding、Reranking、Vector Store
- 承担文档、审计、设置、监控等业务接口

注意：

- 开发态常见端口是 `8000`
- 生产风格常见端口是 `8888`

### 2. `doc-processor`

职责：

- 文档转 Markdown
- PDF 文本提取
- OCR
- 文本切分

常见端口：

- `5003`

说明：

- 当前仓库里它是独立服务，不是 `main-app` 的内嵌模块。
- 与 `main-app` 的调用地址必须通过 `DOC_PROCESSOR_URL` 或等效配置对齐。

### 3. `embedding-service`

职责：

- 为文本生成向量

常见端口：

- 开发风格：`8002`
- Ubuntu/生产风格：`8010`

说明：

- 仓库里保留了不止一种部署约定。
- `main-app` 与它之间的请求/响应格式需要统一，不能只看端口一致。

### 4. `reranking-service`

职责：

- 对检索结果做重排

常见端口：

- 开发风格：`8004`
- Ubuntu/生产风格：`8012`

说明：

- 它属于增强服务，不建议承载唯一业务状态。

### 5. `llm-gateway`

职责：

- 统一多模型提供方入口

说明：

- 当前不在所有部署路径中启用
- 更适合作为扩展能力，而不是默认主链路

### 6. `scheduler`

职责：

- 预留给定时任务、清理、备份等后台任务

说明：

- 当前不是仓库默认主启动链路的一部分
- 旧文档中把它写成 Dify API 调度器的描述已经不再适合作为项目主叙事

## 文档已去掉的失效内容

本次已移除或不再强调以下旧规则：

- 把 `scheduler` 直接写成当前系统主流程的一部分
- 把 `API_URL=http://api:5001` 之类旧 Dify 风格地址当作主链路说明
- 把本目录仅描述成“自定义微服务组件”，忽略主后端的中枢地位

## 相关文档

- [项目入口](../README.md)
- [启动指南](../docs/ONE_CLICK_STARTUP_GUIDE.md)
- [运行依赖分析](../docs/chensha_运行依赖分析.md)
