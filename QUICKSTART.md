# uHomeNest Quickstart (v1.0.0)

Bring up a fresh local stream stack with Jellyfin + minimal API + USXD browser surface.

## 1) Install

```bash
./scripts/install.sh
```

## 2) Start services

```bash
./scripts/start.sh
```

## 3) Health check

```bash
./scripts/healthcheck.sh
curl -sS http://127.0.0.1:7890/api/health
```

Expected response:

```json
{"status":"ok"}
```

## 4) Stop services

```bash
./scripts/stop.sh
```

## 5) Add media

- Add files under `~/media/` using the structure described in `docs/MEDIA_VAULT.md`.
- Re-run the scanner/indexer entrypoint once media changes are made.
