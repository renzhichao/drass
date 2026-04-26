# Reranking Service Migration Guide

> 状态：历史迁移说明，不作为当前服务现状文档。

## 文档定位

这份文件记录的是一轮对 `reranking-service` 的重构迁移思路。它保留有参考价值，但不适合再被当作“当前已完成状态”的主文档。

## 为什么需要降级

旧版内容的问题主要有：

1. 把“迁移目标”写成了“当前事实”。
2. 把若干性能收益、镜像大小收益、部署结果写成已确认结论，但仓库内未提供与之严格绑定的统一验证上下文。
3. 把 `docker-compose`、回滚、监控步骤写成稳定流程，容易让人误解为服务已经形成正式迁移闭环。

## 当前仓库里可确认的事实

当前可以确认：

1. 服务入口文件存在：`app.py`
2. 旧入口/历史实现仍保留：`app_old.py`、`start_service.py`
3. 配置采用环境变量方式，关键变量包括：
   - `RERANKING_PROVIDER`
   - `RERANKING_MODEL`
   - `RERANKING_DEVICE`
   - `RERANKING_MAX_LENGTH`
   - `RERANKING_BATCH_SIZE`
   - `REDIS_URL`
4. 默认监听端口来自配置文件，当前默认值是 `8002`

## 当前更合适的理解方式

应把这份文档理解为：

1. 服务曾经经历过一轮重构和配置收敛。
2. 仓库中同时保留了新旧实现痕迹。
3. 是否真的完成迁移，应以当前代码入口、测试结果和运行方式为准，而不是以这份说明为准。

## 如果你要使用当前服务

优先参考：

1. `services/reranking-service/README.md`
2. `services/reranking-service/config.py`
3. `services/reranking-service/app.py`
4. 服务测试文件与实际启动命令

## 本文件保留用途

保留该文档，仅用于解释历史迁移背景；后续若需要“当前服务说明”，应另写一份面向现状的运行文档，而不是继续沿用这份迁移稿。
