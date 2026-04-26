# 本地 LLM 与 Embedding 说明

这份文档用于说明“本地开发”场景下的两类核心能力：

1. 本地 LLM 服务
2. 本地 Embedding 服务

它不再保留历史机器路径、历史个人目录和一次性操作记录。

## 当前本地开发的常见组合

### 组合 A：MLX LLM + 本地 Embedding

- LLM：`qwen3_api_server.py`
- Embedding：`services/embedding-service/app.py`

常见端口：

- LLM：`8001`
- Embedding：`8002`

### 组合 B：外部 / 独立 AI 服务 + 本地应用层

- LLM：远程或独立本机 `8001`
- Embedding：独立服务 `8010`
- 应用层：`start-api-noproxy.sh` + `start-frontend-only.sh`

## 本地 LLM 说明

当前仓库自带的本地 LLM 入口是：

```bash
python qwen3_api_server.py
```

说明：

- 它提供 OpenAI 兼容接口
- 常见端口为 `8001`
- 依赖 `mlx_lm`
- 依赖本地模型目录

## 本地 Embedding 说明

服务目录：

```bash
services/embedding-service/
```

常见运行方式：

```bash
cd services/embedding-service
python app.py
```

说明：

- 开发态常见端口是 `8002`
- Ubuntu/生产风格文档里也出现过 `8010`
- 当前仓库仍存在两套部署约定，使用时必须先对齐 `main-app` 的访问地址

## 当前必须注意的事实

1. 这两个服务都不是“只要启动就一定兼容主后端”。
2. 端口一致不代表接口契约一致，尤其是 Embedding 服务。
3. 当前项目文档与代码仍在收敛中，应优先参考：
   - `docs/chensha_运行依赖分析.md`
   - `docs/LLM_API_CONFIG_GUIDE.md`

## 已移除的失效内容

本次已去掉：

1. 绑定个人机器路径的说明
2. 一次性部署记录
3. 与当前仓库状态无关的历史性能结论
4. 容易让人误以为接口已经完全对齐的描述
