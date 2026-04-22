# Roadmap Dev Rounds

This plan operationalizes the v1.0.0 brief into near-term rounds.

## Round 1 - Foundation hardening (2-3 days)

- Finalize repo structure and archive boundaries
- Replace API placeholders with modular handlers
- Add deterministic media vault validation and sample fixtures
- Exit criteria:
  - `README.md`, `QUICKSTART.md`, and `docs/` are aligned
  - `tests/ui_smoke_test.sh` and `tests/media_scan_test.sh` pass

## Round 2 - Media indexing core (3-4 days)

- Implement scanner -> indexer pipeline against `~/media/`
- Produce `.media-index.json` with stable schema
- Add search endpoint behavior over generated index
- Exit criteria:
  - `/api/media/browse` and `/api/media/search` return real data
  - `media-vault/validate.sh` is part of setup checks

## Round 3 - Playback and UI integration (3-4 days)

- Wire playback start/stop orchestration paths
- Add USXD runtime loader for launcher/media/now-playing surfaces
- Implement controller navigation bindings (dpad, A/B/X/Y)
- Exit criteria:
  - Browser launcher renders from `ui/usxd/launcher.json`
  - Playback endpoints report actionable state transitions

## Round 4 - Deployment readiness (2-3 days)

- Implement production-grade `scripts/install.sh`
- Add service units and startup dependencies
- Add end-to-end smoke check for install -> start -> health
- Exit criteria:
  - Fresh Ubuntu 22.04/24.04 install passes quickstart flow
  - `curl /api/health` returns `{\"status\":\"ok\"}` post-install

## Round 5 - Sonic Home Express foundation (3-5 days)

- Scaffold `sonic-home-express/` module with `cmd/`, `pkg/`, `scripts/`, and `docs/`
- Define `.she` bundle header/manifest contracts and signing interface
- Add initial pack command skeleton (`pack`, `sign`) with manifest generation
- Exit criteria:
  - `sonic-home-express pack` builds a dev bundle artifact
  - Manifest and signature verification contracts are documented

## Round 6 - Sonic Home Express install/distribution lane (4-6 days)

- Add install flow skeleton (`install`, `verify`) with dry-run support
- Add LAN channel serve skeleton (`serve`) and channel manifest contract
- Add USB auto-install scripts and preseed config template
- Exit criteria:
  - Install dry-run reports actionable component plan
  - Local update server exposes stable/beta/edge metadata

## Round 7 - Sonic compatibility and hardening (3-4 days)

- Add compatibility adapter for future full Sonic-family tool detection
- Add smoke tests for pack -> verify -> install (dry-run) flow
- Document operator workflow and upgrade-to-full-Sonic guidance
- Exit criteria:
  - Lite-to-full Sonic upgrade path is documented and test-covered at contract level
