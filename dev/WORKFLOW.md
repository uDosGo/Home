# Workflow (v1)

## 1. Plan

- Read `docs/ROADMAP.md`
- Pick current round from `dev/ROADMAP-ROUNDS.md`
- Update active item in `TASKS.md`

## 2. Build

- Implement minimal vertical slices under `server/`, `ui/`, `media-vault/`
- Keep scripts in `scripts/` runnable on Ubuntu

## 3. Validate

- Run `tests/ui_smoke_test.sh`
- Run `tests/media_scan_test.sh`
- Run `tests/health_test.sh` (when API is running)

## 4. Document

- Update `CHANGELOG.md`
- Update relevant docs under `docs/`
