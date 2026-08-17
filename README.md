# IntegrationsMono
for 3P app, adapters and config

## Dev stack

Start Redis, simulation publisher, and C2:

```bash
docker compose -f environments/dev/docker-compose.yml up --build
```

Open http://127.0.0.1:8000 — click **Say hello**.

Stop:

```bash
docker compose -f environments/dev/docker-compose.yml down
```

### Local C2 (Redis/sim still in Docker)

```bash
docker compose -f environments/dev/docker-compose.yml up --build cots-hardware simulation-publisher
source .venv/bin/activate
COTS_HOST=localhost COTS_PORT=6379 uvicorn c2.api.app:app --reload --app-dir .
```

## Redis image ingest

```bash
GITHUB_ORG=acme REDIS_VERSION=7.2.4 bash -lc 'source ingestion/redis/ingest.sh'
```
