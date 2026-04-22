# Composting legacy docs and scripts (`.compost/`)

**`.compost/`** at the repo root is **gitignored**. Use it for **local** copies of superseded files after you remove them from Git — not as a second source of truth.

## When to compost

- You merged content into a newer doc and the old file is redundant.
- You replaced a one-off script with a maintained path under `scripts/`.
- You need a timestamped backup before a risky delete (copy here first).

## Cleanup **2026-04-10** (v4 focus)

The following were **copied** to **`.compost/cleanup-2026-04-10/`** (if you ran the cleanup on this machine) and **removed from Git**:

| Removed from Git | Notes |
| --- | --- |
| `docs/architecture/PHASE-*.md`, `server/docs/architecture/PHASE-*.md` | Pre-v4 milestone session reports |
| `docs/architecture/UHOME-SERVER-DEV-PLAN.md` (old), same under `server/docs/` | Replaced by slim **v4** [`docs/architecture/UHOME-SERVER-DEV-PLAN.md`](../docs/architecture/UHOME-SERVER-DEV-PLAN.md) |
| `docs/MIGRATION-STATUS.md`, `docs/ROADMAP-STATUS-2026-03-10.md` (+ `server/docs/` copies) | Historical migration / status snapshots |
| `@dev/`, `server/@dev/`, `matter/@dev/`, `host/@dev/` | Binder-era dev rounds (duplicate trees) |
| `dev/archive-uHOME-app-*.md` | Tombstone notes for removed app checkouts |
| `structure-uhome.txt` | Legacy structure dump |
| Root `uhome/` package | Unused FastAPI scaffold (8788); runtime is `src/uhome_server/` |

**Canonical v4 docs:** [`docs/ROADMAP-V4.md`](../docs/ROADMAP-V4.md), [`docs/README.md`](../docs/README.md).

Do **not** compost secrets, production configs, or anything that must stay in backup outside the repo.

## One-liner (example)

```bash
mkdir -p .compost/$(date +%Y%m%d) && cp path/to/old-file.md .compost/$(date +%Y%m%d)/
```

After verifying the copy, remove the original in a normal commit.
