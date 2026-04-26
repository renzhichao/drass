# Unified LLM Service Migration Guide

> 状态：历史迁移说明，不作为当前主后端的权威服务说明。

## 文档定位

这份文件原本用于说明主后端从旧 LLM 调用方式迁移到 `llm_service_enhanced.py` 的设计与接入思路。它属于阶段性迁移材料，不适合继续承担“当前实现说明”职责。

## 为什么需要降级

旧版内容存在几个容易误导的点：

1. 把增强服务能力写成已经完全落地的统一现状。
2. 混合了历史迁移步骤、示例代码、未来能力和测试建议。
3. 使用了多套 provider 叙事，容易让读者误以为所有路径都已在项目主链路上同等稳定。

## 当前仓库里可确认的事实

当前可以直接确认：

1. `llm_service.py` 与 `llm_service_enhanced.py` 同时存在。
2. `unified_llm_service` 已在若干运行路径中被引用。
3. 主配置项仍以以下变量为核心：
   - `LLM_PROVIDER`
   - `LLM_BASE_URL`
   - `LLM_API_KEY`
   - `LLM_MODEL`
4. 代码里仍保留了 LM Studio、OpenRouter、OpenAI-compatible 等多种兼容路径。

## 当前更准确的理解方式

这说明主后端的 LLM 能力已经朝统一抽象演进，但仓库仍保留历史兼容层与多种接入模式。是否应切换、如何切换，不能只依据这份迁移文档判断，而要结合：

1. `services/main-app/app/core/config.py`
2. `services/main-app/app/services/llm_service.py`
3. `services/main-app/app/services/llm_service_enhanced.py`
4. `docs/LLM_API_CONFIG_GUIDE.md`

## 当前建议

1. 把这份文件视为历史迁移背景。
2. 新的环境配置和部署说明，应优先使用项目根文档与 `docs/` 下已校正的 LLM 配置说明。
3. 若要形成真正的“当前 LLM 服务说明”，应单独写一份面向现状的运行文档，而不是继续扩展这份迁移稿。
