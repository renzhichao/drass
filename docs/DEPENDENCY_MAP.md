# Drass System Dependency Map

> SSOT — Last updated: 2026-04-26

## Service Dependency Graph

```mermaid
graph TD
    %% ── User ──────────────────────────────────────────────
    USER(["👤 User Browser"])

    %% ── Frontend ──────────────────────────────────────────
    subgraph FE_LAYER["Frontend  ·  React 18 + TypeScript  ·  Vite"]
        FE["frontend\n:5173\nRedux Toolkit · MUI v5\nAxios · Socket.io-client\nreact-router-dom · react-query"]
    end

    %% ── Backend API ───────────────────────────────────────
    subgraph BE_LAYER["Backend API  ·  Python / FastAPI"]
        MA["main-app\n:8000\nFastAPI · LangChain · OpenAI SDK\nRAG Chain · Agent · Auth (JWT)\nWebSocket · Rate Limiting"]
        LG["llm-gateway  [optional]\n:8003\nMulti-provider LLM routing\nOpenRouter · Qwen3 · Ollama"]
    end

    %% ── Microservices ─────────────────────────────────────
    subgraph SVC_LAYER["Microservices  ·  Python"]
        EMB["embedding-service\n:8002\nFastAPI · sentence-transformers\nModel: BAAI/bge-base-en-v1.5"]
        RNK["reranking-service\n:8004\nFastAPI · sentence-transformers\nModel: cross-encoder/ms-marco-MiniLM-L-12-v2"]
        DP["doc-processor\n:5003\nFlask · pypdf · python-docx\nopenpyxl · pytesseract (OCR)\nPDF · DOCX · XLSX · PPTX"]
        SCH["scheduler  [optional]\n:standalone\nAPScheduler · Task orchestration"]
    end

    %% ── Infrastructure ────────────────────────────────────
    subgraph INFRA_LAYER["Infrastructure  ·  Stateful Services"]
        PG[("PostgreSQL :5432\nUsers · Sessions\nAudit Logs")]
        RD[("Redis :6379\nCache · Rate Limits\nSession Store")]
        CD[("ChromaDB\nVector Store\nDocument Embeddings")]
    end

    %% ── Local / External LLM ──────────────────────────────
    subgraph LLM_LAYER["LLM Providers"]
        QWEN["Qwen3-8B-MLX\nmlx_lm.server  :8001\nApple Silicon (MLX)"]
        OR["OpenRouter\nCloud API\ngpt-4 · claude · etc."]
        OL["Ollama\nLocal fallback\nqwen2.5:7b"]
        HF["HuggingFace Hub\nModel registry\n(download only)"]
    end

    %% ── Monitoring ────────────────────────────────────────
    subgraph MON_LAYER["Monitoring  ·  docker profile: monitoring"]
        PROM["Prometheus :9090\nMetrics scraping"]
        GRAF["Grafana :3001\nDashboards"]
    end

    %% ══════════════════════════════════════════════════════
    %% Edges — User → Frontend → Backend
    %% ══════════════════════════════════════════════════════
    USER -->|"HTTPS"| FE
    FE -->|"REST API + WebSocket"| MA

    %% Backend → Microservices
    MA -->|"HTTP POST /embed"| EMB
    MA -->|"HTTP POST /rerank"| RNK
    MA -->|"HTTP POST /process"| DP

    %% Backend → Infrastructure
    MA -->|"PostgreSQL (asyncpg)"| PG
    MA -->|"Redis (cache/sessions)"| RD
    MA -->|"ChromaDB client"| CD

    %% Backend → LLM (via gateway or direct)
    MA -->|"OpenAI-compat API"| LG
    MA -.->|"Direct fallback"| QWEN

    %% LLM Gateway → Providers
    LG -->|"OpenAI-compat :8001"| QWEN
    LG -->|"HTTPS"| OR
    LG -->|"HTTP :11434"| OL

    %% Microservices → Infrastructure
    EMB -->|"Redis (embedding cache)"| RD
    RNK -->|"Redis (score cache)"| RD
    SCH -->|"Redis (job state)"| RD

    %% Monitoring → Services
    PROM -.->|"Scrape /metrics"| MA
    PROM -.->|"Scrape /metrics"| EMB
    PROM -.->|"Scrape /metrics"| RNK
    GRAF -->|"PromQL"| PROM

    %% Model downloads (one-time, dashed)
    EMB -.->|"Download on startup"| HF
    RNK -.->|"Download on startup"| HF
```

---

## Layer Summary

| Layer | Services | Ports | Key Tech |
|-------|----------|-------|----------|
| **Frontend** | frontend | 5173 | React 18, Redux Toolkit, MUI, Socket.io |
| **Backend API** | main-app | 8000 | FastAPI, LangChain, OpenAI SDK, JWT |
| **Backend API** | llm-gateway *(opt)* | 8003 | FastAPI, multi-provider LLM routing |
| **Microservices** | embedding-service | 8002 | sentence-transformers, BAAI/bge |
| **Microservices** | reranking-service | 8004 | sentence-transformers, cross-encoder |
| **Microservices** | doc-processor | 5003 | Flask, pypdf, pytesseract |
| **Microservices** | scheduler *(opt)* | — | APScheduler |
| **Infrastructure** | PostgreSQL | 5432 | User data, audit logs |
| **Infrastructure** | Redis | 6379 | Cache, sessions, rate limits |
| **Infrastructure** | ChromaDB | 8000 | Vector store (document embeddings) |
| **LLM** | Qwen3-8B-MLX | 8001 | mlx_lm.server, Apple Silicon |
| **LLM** | OpenRouter | HTTPS | Cloud: GPT-4, Claude, etc. |
| **LLM** | Ollama | 11434 | Local alternative |
| **Monitoring** | Prometheus | 9090 | Metrics scraping |
| **Monitoring** | Grafana | 3001 | Dashboards (depends on Prometheus) |

---

## Hard Dependencies (docker `depends_on`)

```
frontend         → main-app
main-app         → postgres, redis, chromadb, embedding-service, reranking-service, doc-processor
embedding-service → redis
reranking-service → redis, postgres
llm-gateway      → redis
grafana          → prometheus
```

---

## Legend

| Arrow | Meaning |
|-------|---------|
| `→` (solid) | Runtime hard dependency |
| `-.->` (dashed) | Optional / one-time / fallback |
