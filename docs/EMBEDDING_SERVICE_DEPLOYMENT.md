# Embedding 服务部署说明

本文档只说明当前项目里 Embedding 服务的角色、常见端口和部署注意事项，不再保留过度展开的通用选型内容。

## 服务角色

Embedding 服务负责把文本转换为向量，供：

- 文档入库
- 向量检索
- RAG 查询

主调用方通常是：

- `services/main-app/app/services/embedding_service.py`
- `services/main-app/app/services/vector_store.py`

## 当前常见端口

仓库中目前存在两套常见约定：

### 开发态

- 服务端口：`8002`

### Ubuntu / 生产风格

- 服务端口：`8010`

因此部署前必须先明确你走的是哪条路径，再同步：

- `EMBEDDING_API_BASE`
- 启动脚本
- Nginx / 监控 / 健康检查

## 常见运行方式

### 本地运行

```bash
cd services/embedding-service
python app.py
```

### 容器运行

参考：

- `services/embedding-service/Dockerfile`
- 根目录 `docker-compose.yml`

## 当前配置建议

推荐优先使用：

```bash
EMBEDDING_PROVIDER=sentence-transformers
EMBEDDING_MODEL=BAAI/bge-large-zh-v1.5
EMBEDDING_API_BASE=http://localhost:8002
```

如果是 Ubuntu/独立 AI 服务风格：

```bash
EMBEDDING_PROVIDER=openai
EMBEDDING_MODEL=Qwen3-Embedding-8B
EMBEDDING_API_BASE=http://localhost:8010/v1
EMBEDDING_API_KEY=123456
```

## 当前最重要的风险点

当前仓库里，Embedding 服务的最大问题不是“怎么启动”，而是“接口是否对齐”：

1. `main-app` 的请求体和返回体预期需要与服务实现核对。
2. 历史文档里有些内容默认认为服务已经完全兼容，这不可靠。
3. 只修改端口不修改协议，主链路仍可能失败。

## 已移除的失效内容

本次已去掉：

1. 过长的通用 provider 选型介绍
2. 与当前项目无关的大量性能优化示例
3. 把 `8001` 长期写成 Embedding 主端口的旧说明
4. 未与当前主后端契约核对就直接给出的集成示例
