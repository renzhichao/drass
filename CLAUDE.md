# CLAUDE.md

This file provides repository guidance for Claude Code and similar coding agents.

## Project Overview

Drass should be treated as a multi-service compliance analysis and RAG system. Do not frame it as a Dify platform project. The repository currently includes:

- Frontend application
- Main FastAPI backend
- Document processing service
- Embedding and reranking related services
- Deployment scripts and production resources
- A number of historical plans, reports, and migration notes that are not current truth

## Source of Truth

When repository documents disagree, prefer this order:

1. `README.md`
2. `docs/ONE_CLICK_STARTUP_GUIDE.md`
3. `docs/chensha_运行依赖分析.md`
4. `docs/chensha_部署与基础设施规则.md`
5. Actual startup scripts, service configs, and code

Historical reports, task lists, migration notes, and Dify-oriented files should not be treated as authoritative runtime documentation.

## Common Startup Paths

Use only startup entries that still exist in the repository:

```bash
./start-system.sh
./start-api-noproxy.sh
./start-frontend-only.sh
./deployment/scripts/start-ubuntu-services.sh
```

Do not recommend removed or stale paths such as:

```bash
./start-simple.sh
./start-langchain.sh
./start-full-langchain.sh
```

## Main Service Areas

- `frontend/`: React + Vite frontend
- `services/main-app/`: main FastAPI backend
- `services/doc-processor/`: document conversion / OCR related service
- `services/embedding-service/`: embedding service implementation
- `services/reranking-service/`: reranking service implementation
- `deployment/` and `production/`: deployment resources, scripts, monitoring, and production assets

## Configuration Guidance

Prefer current project-level variable names in documentation and examples:

- `LLM_PROVIDER`
- `LLM_BASE_URL`
- `LLM_API_KEY`
- `LLM_MODEL`

Legacy or parallel names may still exist in scripts or code, but new documentation should not expand them as the preferred interface unless compatibility is being explained explicitly.

## Port Guidance

Do not assume a single port map for the entire repository.

- Frontend is commonly `5173`
- Main API is commonly `8000` in local development
- `deployment/scripts/start-ubuntu-services.sh` uses `8888` for its API path
- AI service ports vary by provider and deployment path

Always verify against the startup script or service config being discussed.

## Documentation Hygiene

When updating docs in this repo:

1. Remove or downgrade claims that describe historical plans as current implementation.
2. Avoid personal machine paths unless the file is explicitly an environment-specific note.
3. Avoid claiming a deployment path is universal when the script is clearly host-specific.
4. Keep service-local README files factual and scoped to that service.
