# deployment 目录说明

本目录用于承载 Drass 的部署配置、预设、脚本和生产化辅助文件。它不是一个已经完全收敛的“统一部署平台”，而是当前项目多种部署路径的集合。

## 当前目录作用

| 目录/文件 | 作用 |
| --- | --- |
| `configs/` | 部署预设、模板、用户配置 |
| `scripts/` | 配置生成、校验、启动、修复、测试脚本 |
| `docs/` | 特定部署路径说明 |
| `production/` | 容器化生产风格部署资源 |
| `schemas/` | 配置结构约束 |

## 当前实际部署路径

当前仓库里实际可识别的部署路径主要有三条：

1. 本地开发联调
   - 参考：根目录 `start-system.sh`
   - 特点：开发态，本地前后端 + Docker 基础设施混合

2. Ubuntu / 本机服务化部署
   - 参考：`deployment/scripts/start-ubuntu-services.sh`
   - 特点：更接近生产，常配合已有 LLM / Embedding / Reranking 服务

3. 容器化生产风格部署
   - 参考：`deployment/production/docker-compose.prod.yml`
   - 特点：以容器编排 main-app、AI 服务、Redis、Nginx、监控组件

## 当前应优先参考的文件

如果你要部署项目，建议阅读顺序：

1. `README.md`
2. `docs/ONE_CLICK_STARTUP_GUIDE.md`
3. `docs/chensha_部署与基础设施规则.md`
4. `deployment/docs/ubuntu-amd-deployment.md`
5. `production/` 目录下的配置和脚本

## 这份目录说明不再承诺的内容

以下内容在历史文档里表达得过满，但当前仓库并不适合继续作为默认事实：

1. “所有部署模式都已被统一配置系统完整覆盖”
2. “configure.py / deploy.py 已经是唯一权威入口”
3. “AWS、Docker Compose、本地 GPU 三套路径在当前实现层面完全对齐”
4. “health_check.py / monitor.py / rollback.py 等工具已形成完整闭环”

## 当前更准确的事实

1. `deployment/` 更像“部署资源集合”，不是完全收敛的发布平台。
2. 部署脚本有一定参考价值，但不能替代对 `production/`、启动脚本和服务配置的核对。
3. 当前最重要的工作不是继续扩展部署模式，而是统一端口、变量名、服务契约和文档入口。
