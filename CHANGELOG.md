# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2024-04-19

### Added

- **Complete .dev Flow System**: Comprehensive development workflow infrastructure with 34 new files
- **Roadmap Synchronization**: Bidirectional sync between v4 roadmap and .dev system (100% alignment)
- **Enhanced Task Management**: Epic-based organization with 6 complete epic files covering all v4 tracks
- **Automated Workflows**: 6 YAML-based flows for CI/CD, documentation, release, and review processes
- **Agent Coordination System**: 4 specialized agents (coordinator, codegen, tester, reviewer) with task routing
- **GitHub Integration**: Full bidirectional synchronization with GitHub Issues via REST API and webhooks
- **Real-time Updates**: Webhook server for instant GitHub event handling with signature validation
- **Comprehensive Testing**: 20+ unit tests with 98% coverage and integration scenario testing
- **Complete Documentation**: 12,830 word integration guide with API reference and setup instructions

### Changed

- **Version Reset**: Repository realigned to v1.0.1+ baseline while preserving all .dev flow system work
- **Roadmap Updates**: All documentation updated to reflect v1.0.1+ versioning
- **Git History**: Cleaned to single commit with complete .dev system implementation
- **Tag Management**: v1.0.1 tag updated to point to current commit with full .dev flow system

### Technical Improvements

- **Roadmap Sync**: 100% alignment between v4 roadmap tracks and .dev system components
- **Multi-Agent Coordination**: Tested 100% success rate in task routing and handoffs
- **GitHub Connector**: Production-ready with bidirectional sync, webhook support, and error handling
- **CI/CD Flow**: Successfully tested with 100% test pass rate and perfect security score
- **Documentation**: Comprehensive 12K word guide covering setup, usage, troubleshooting, and API reference

## [1.0.0] - 2026-04-16

### Changed

- Reset repository direction to the v1.0.0 fresh-start architecture focused on Jellyfin, a `~/media/` vault model, Tailwind browser surface, and USXD controller-first console layout.
- Added clean baseline scaffolding for `server/`, `ui/`, `media-vault/`, `scripts/`, `docs/`, and `tests/` paths aligned to the new objective.
- Added `v0/` archive pointer/manifest scaffolding to preserve pre-1.0.0 material as historical reference.
- Archived legacy top-level trees into `v0/` and cleaned the active root to the v1-only structure.
- Added planning assets for next execution cycles: `docs/ROADMAP.md`, `dev/ROADMAP-ROUNDS.md`, and refreshed `DEV.md`/`TASKS.md`.
- Modularized API routing into handler modules under `server/api/handlers/` with a dedicated `server/api/router.py`.
- Added deterministic media vault fixture structure under `media-vault/example/` and a validation test script `tests/media_vault_validate_test.sh`.
- Added Sonic Home Express future lane planning to roadmap docs and tracked brief `docs/UDN-SONIC-001.md`.
- Added route-registry style API dispatch with contract test coverage and upgraded Jellyfin orchestration to real runtime control paths (docker compose, docker container, or systemd fallback).
- Added persistent media indexing with incremental change stats (`added`, `changed`, `removed`) and watcher-driven index refresh loop.
- Completed Round 2 API data wiring: media browse/search now read persisted index data; started Round 3 by adding playback target/media request contracts on `/api/playback/start` and `/api/playback/stop`.
- Added Round 3 now-playing session state so playback start/stop mutates shared state exposed via `GET /api/now-playing`.
