# LM Studio 部署说明

LM Studio 在当前项目中属于“可选本地 LLM 提供方”，不是唯一或默认的项目主线。它应被理解为 OpenAI 兼容接口的一种本地实现。

## 适用场景

适合：

- macOS 本地开发
- 想通过图形界面管理模型
- 不想直接维护底层推理命令

不适合直接作为：

- 当前项目唯一权威部署路径
- Ubuntu 生产风格部署主方案

## 当前接入方式

LM Studio 的接入方式应统一到：

```bash
LLM_PROVIDER=openai
LLM_BASE_URL=http://localhost:1234/v1
LLM_API_KEY=not-required
LLM_MODEL=local-model
```

也就是说：

- `main-app` 不需要知道“这是 LM Studio”
- `main-app` 只需要知道“这是一个 OpenAI 兼容接口”

## 启动建议

1. 在 LM Studio 中下载并加载本地模型
2. 启动本地 OpenAI-compatible server
3. 确认服务监听 `1234`
4. 再让 `main-app` 指向 `LLM_BASE_URL=http://localhost:1234/v1`

## 当前项目中的位置

LM Studio 相关说明仅适合作为以下路径的补充：

- `README.md`
- `docs/LLM_API_CONFIG_GUIDE.md`
- 本地开发试验场景

如果是当前仓库更典型的运行方式，优先看的还是：

- `qwen3_api_server.py`
- `start-system.sh`
- `start-api-noproxy.sh`

## 已移除的失效内容

这次已去掉：

1. 把 LM Studio 描述成已完全替代其他 LLM 方案的叙述
2. 绑定旧个人目录的命令示例
3. 与当前项目主线无关的长篇性能和客户端示例
4. 容易让人误以为仓库当前默认就是 `1234` 端口的描述
