# IntegrationsMono
for 3P app, adapters and config

## Dev stack

Start (builds the simulation publisher if needed):

```bash
docker compose -f environments/dev/docker-compose.yml up --build
```

Stop:

```bash
docker compose -f environments/dev/docker-compose.yml down
```

## Redis image ingest

```bash
GITHUB_ORG=acme REDIS_VERSION=7.2.4 bash -lc 'source ingestion/redis/ingest.sh'
```
