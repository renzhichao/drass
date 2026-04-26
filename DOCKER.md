# Docker 说明

> 状态：历史 Docker 路径说明，不再代表当前 Drass 的默认部署事实。

这份文件之前把项目描述成“Drass Dify Platform”的完整 Docker 部署手册，但当前仓库的主线已经不是 Dify 平台封装，也没有证据表明这里仍存在一套可直接照抄执行的完整 Dify 容器方案。

## 为什么需要降级

旧版内容存在几个明显问题：

1. 把项目主定位写成 Dify 平台，与当前多服务合规 / RAG 系统不符。
2. 把 `api:5001`、`web:3000`、`weaviate:8080` 当作当前默认主链路端口，这与现仓库主入口不一致。
3. 把不存在或未确认的脚本、默认账号和完整容器拓扑写成已验证事实，误导性较强。

## 当前更准确的事实

当前仓库可确认的部署路径主要是：

1. 本地开发联调
   - 入口参考：`./start-system.sh`
   - 补充入口：`./start-api-noproxy.sh`、`./start-frontend-only.sh`

2. Ubuntu / 机器内服务化启动
   - 入口参考：`deployment/scripts/start-ubuntu-services.sh`
   - 特点：更偏环境脚本，依赖宿主机已有服务和目录约束

3. 容器化生产风格资源
   - 入口参考：`deployment/production/docker-compose.prod.yml`
   - 特点：属于生产化部署资源集合，不能简单等同于“一键完整平台”

## 当前建议阅读顺序

1. `README.md`
2. `docs/ONE_CLICK_STARTUP_GUIDE.md`
3. `docs/chensha_部署与基础设施规则.md`
4. `deployment/README.md`
5. `deployment/production/`

## 本文件保留用途

本文档仅保留为历史线索，提醒仓库里曾存在一套偏 Dify 叙事的 Docker 思路。后续若要整理容器化方案，应基于当前 `production/` 配置、真实服务端口和现有启动脚本重新编写，而不是继续沿用旧版 Dify 说明。
