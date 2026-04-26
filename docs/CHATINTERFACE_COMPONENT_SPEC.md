# 聊天界面组件说明

> 状态：已从“未来功能规范”收敛为“当前前端实现对照说明”。

这份文档只描述当前仓库里可以确认的聊天相关组件，不再继续扩写一个尚未完整落地的通用 ChatInterface 规范。

## 当前能确认的聊天相关组件

仓库中当前最直接的聊天组件是：

- `frontend/src/components/SimpleChatInterface.tsx`

与聊天相关的周边能力还包括：

- `frontend/src/components/DocumentUpload/`
- `frontend/src/components/DocumentDashboard/`
- `frontend/src/components/KnowledgeBase/`
- `frontend/src/components/AuditLogs/`

## 当前聊天组件事实

### `SimpleChatInterface`

当前实现特征：

1. 单页聊天界面
2. 使用 Material UI
3. 消息结构简单，包含：
   - `id`
   - `role`
   - `content`
   - `timestamp`
4. 支持 Markdown 渲染
5. 当前通过 HTTP 请求调用后端测试聊天接口

当前代码里可直接确认的行为：

- 用户消息和助手消息分左右显示
- 回答支持 Markdown
- 有基本的打字机效果
- 请求目标为 `http://localhost:8888/api/v1/test/chat`

## 当前不应再默认承诺的能力

以下内容在旧规范里写得很完整，但当前仓库里不能直接把它们当成既成事实：

1. 完整会话侧边栏体系
2. 完整的模板命令系统
3. 完整的引用溯源 UI
4. 完整的 WebSocket 流式聊天闭环
5. 完整的统一 ChatInterface 组件族

这些能力里有些可能有部分实现，有些只是设计意图，但当前文档不再默认视为已落地。

## 当前更准确的前端理解

项目前端不是“单一聊天产品”，而是“聊天 + 文档 + 审计 + 知识库 + 监控”的组合界面。

因此聊天相关文档应遵守两条原则：

1. 只描述仓库里能找到的组件
2. 不把未来规划写成当前事实

## 如果后续要继续完善这份文档

建议按真实代码逐步补充：

1. `SimpleChatInterface` 的当前 props 和状态
2. 与文档上传、知识库的真实交互关系
3. 当前是否已接入正式聊天路由，而不是测试接口
