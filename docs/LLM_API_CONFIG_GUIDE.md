# LLM API 配置指南

本文档只保留当前项目仍然相关的 LLM 接入方式，并对齐仓库里的真实变量名和常见部署路径。

## 当前支持的主路径

### 1. OpenAI 兼容接口

这是当前项目最核心的接入方式。无论后端实际接的是本地 MLX、vLLM、LM Studio 还是其他兼容网关，`main-app` 主要都通过 OpenAI 兼容接口访问。

推荐变量：

```bash
LLM_PROVIDER=openai
LLM_BASE_URL=http://localhost:8001/v1
LLM_API_KEY=123456
LLM_MODEL=vllm
```

适用：

- `qwen3_api_server.py`
- vLLM OpenAI API
- LM Studio OpenAI-compatible server

### 2. OpenRouter

如果不走本地模型，可以用 OpenRouter 作为云端 LLM 提供方。

```bash
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=your_key
LLM_MODEL=anthropic/claude-3.5-sonnet
```

适用：

- 不想维护本地模型服务
- 仅做 API 方式验证

### 3. LM Studio

LM Studio 仍然是可选路径，但它不再单独代表“项目默认 LLM 方案”，而只是 OpenAI 兼容接口的一种实现。

```bash
LLM_PROVIDER=openai
LLM_BASE_URL=http://localhost:1234/v1
LLM_API_KEY=not-required
LLM_MODEL=local-model
```

### 4. vLLM

Ubuntu / GPU 部署场景常见：

```bash
LLM_PROVIDER=openai
LLM_BASE_URL=http://localhost:8001/v1
LLM_API_KEY=123456
LLM_MODEL=vllm
```

## 当前项目应优先使用的变量名

当前建议统一使用：

- `LLM_PROVIDER`
- `LLM_BASE_URL`
- `LLM_API_KEY`
- `LLM_MODEL`

不建议继续在文档里把这些变量并列写成多个互相竞争的主入口：

- `OPENAI_API_BASE`
- `VLLM_BASE_URL`
- `LMSTUDIO_BASE_URL`

如果历史脚本仍使用这些变量，应在启动脚本中做映射，而不是继续扩散到新文档。

## 常见部署场景

### 本地开发

```bash
LLM_PROVIDER=openai
LLM_BASE_URL=http://localhost:8001/v1
LLM_API_KEY=not-required
LLM_MODEL=qwen3-8b-mlx
```

### Ubuntu / 独立 AI 服务

```bash
LLM_PROVIDER=openai
LLM_BASE_URL=http://localhost:8001/v1
LLM_API_KEY=123456
LLM_MODEL=vllm
```

### 云端 API

```bash
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=your_key
LLM_MODEL=anthropic/claude-3.5-sonnet
```

## 已移除的失效内容

这次从文档里去掉了：

1. 把所有本地模型方案都写成同等推荐主路径的做法
2. 过细但未与当前仓库启动脚本对齐的安装教程
3. 混用 `OPENAI_API_BASE` 与 `LLM_BASE_URL` 的主配置写法
4. 与当前项目主线无关的超长选型说明

## 相关文档

- `README.md`
- `docs/ONE_CLICK_STARTUP_GUIDE.md`
- `docs/LMSTUDIO_DEPLOYMENT_GUIDE.md`
- `docs/chensha_运行依赖分析.md`
