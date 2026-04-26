# DevOps / Infra Rules

This file is the canonical human-readable source of truth for Drass DevOps and infrastructure rules.

Scope:
- Deployment topology selection
- Required infrastructure components
- Environment-specific constraints
- Security, networking, monitoring, and operations baselines

Implementation note:
- Runtime validation still exists in `deployment/schemas/config-schema.yaml` and `deployment/scripts/utils/config_models.py`.
- Where code and historical presets/scripts diverge, this file is the intended rule baseline to align future cleanup work against.

## 1. Supported Deployment Modes

Only the following deployment modes are supported:

- `docker-compose`
  - Primary use: local development and integration testing
  - Characteristics: containerized stack, reproducible local environment
- `local-gpu`
  - Primary use: single-machine accelerated deployment
  - Characteristics: Apple Silicon MLX or NVIDIA/AMD local model serving
- `aws`
  - Primary use: cloud production deployment
  - Characteristics: managed infrastructure, regional deployment, external networking
- `kubernetes`
  - Primary use: orchestrated multi-instance deployment
  - Characteristics: explicit scaling and service orchestration

## 2. Environment Rules

Only the following environments are valid:

- `development`
- `staging`
- `production`

Environment baselines:

- `development`
  - May disable monitoring, rate limits, and strict security controls for local iteration
  - Should prefer local or low-cost dependencies
- `staging`
  - Must be operationally close to production
  - Should exercise health checks, logging, and service connectivity before release
- `production`
  - Must enable monitoring
  - Must enable encryption
  - Must define scaling behavior or a deliberate single-node exception
  - Must use managed or persistent backing services for stateful data

## 3. Required Core Services

The platform is built around these core service domains:

- API backend
- Frontend
- LLM service
- Embedding service
- Reranking service
- Vector store
- Database
- Cache

Minimum operational baseline:

- `llm` should be configured for any usable deployment
- `database` should be configured for all shared or persistent environments
- `vector_store` should be configured for all RAG-enabled environments
- `cache` is strongly recommended for any non-trivial deployment

## 4. Deployment-Specific Constraints

### `docker-compose`

- Intended for local development or test environments
- Should include:
  - database service
  - cache service
  - vector store service when RAG is enabled
- Should generate a local `.env`
- Should expose only the ports required for local use

### `local-gpu`

- Requires GPU capability to be explicitly enabled in configuration
- Should use a local model provider:
  - `local-mlx`
  - `vllm`
  - `ollama`
- Should keep model endpoints on localhost or private network interfaces unless a reverse proxy is intentionally configured

### `aws`

- Requires `deployment.region`
- Should define domain and ingress strategy
- Should prefer managed stateful services such as RDS and ElastiCache where practical
- Secrets should not be hardcoded in preset files

### `kubernetes`

- Requires an explicit scaling strategy
- Should define ingress, service exposure, and persistent volume behavior
- Should not rely on mutable local filesystem state for durable application data

## 5. Provider Rules

### LLM Providers

Allowed providers:

- `openrouter`
- `openai`
- `local-mlx`
- `vllm`
- `ollama`
- `azure`

Rules:

- Cloud providers must supply an API key
- Local GPU deployments should prefer local providers over cloud providers
- Production deployments should pin model identifiers intentionally rather than relying on vague defaults

### Embedding Providers

Allowed providers:

- `openai`
- `cohere`
- `local`
- `sentence-transformers`

Rules:

- Local development should prefer local embeddings unless there is a clear need for remote embeddings
- Embedding dimensions and model choice should remain compatible with the selected vector store collections

### Stateful Backing Services

Allowed providers by domain:

- Vector store: `chromadb`, `weaviate`, `pinecone`, `qdrant`, `milvus`
- Database: `postgresql`, `mysql`, `mongodb`
- Cache: `redis`, `memcached`, `dynamodb`

Rules:

- Production data must use persistent storage
- Local-only in-memory caches are acceptable for development, not for production
- Database connection pools must be sized intentionally for production workloads

## 6. Networking Rules

- Every exposed service port must be intentional
- Public exposure should be limited to frontend, API, and managed ingress endpoints
- Internal services such as embeddings, reranking, vector store, cache, and database should remain private by default
- TLS should be enabled for public production traffic
- Load balancers, when used, must be one of:
  - `alb`
  - `nlb`
  - `nginx`
  - `traefik`

## 7. Security Rules

- Encryption defaults to enabled
- Secrets must not be committed as real values in presets, examples, or production configs
- Supported secrets backends are:
  - `aws-secrets`
  - `vault`
  - `local`
  - `kubernetes`
- Firewall rules, if declared, must specify:
  - port
  - protocol
  - source
- Production should keep externally reachable ports to the minimum required surface area

## 8. Monitoring and Logging Rules

- Production monitoring must be enabled
- Supported monitoring providers are:
  - `prometheus`
  - `grafana`
  - `cloudwatch`
  - `datadog`
  - `newrelic`
- Logging levels must be one of:
  - `DEBUG`
  - `INFO`
  - `WARNING`
  - `ERROR`
  - `CRITICAL`
- Production should emit structured logs and retain enough metrics for health, latency, throughput, and failure analysis

## 9. Health and Operability Rules

- Deployments should provide health checks for long-running services
- Startup order must respect dependencies between API, stateful services, and model-serving services
- Generated environment files should be derived from validated configuration
- Failed deployments should stop cleanly and avoid leaving half-configured state where possible

## 10. Configuration Governance

Canonical governance rules:

- New deployment behavior should be added only if it can be expressed in:
  - this file
  - `deployment/schemas/config-schema.yaml`
  - `deployment/scripts/utils/config_models.py`
- Presets must conform to these rules
- Historical scripts or presets that diverge from this file should be treated as technical debt, not as alternate truth sources

Current cleanup targets already visible in the repository:

- Some presets use legacy keys like `type`, `application`, and `document_processor`
- Some runtime code in `deployment/scripts/deploy.py` still consumes that older shape

Until that cleanup is complete, use this file as the policy baseline for reviews and future refactors.
