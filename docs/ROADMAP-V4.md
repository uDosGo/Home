# uHOME / uHomeNest — v4 plan (canonical)

**Repository:** **uHomeNest v3.9** (**3.9.x** in [`VERSION`](../VERSION)). **Single planning surface** for the uHOME product line inside this monorepo. Execution detail lives in **issues** and **[`TASKS.md`](../TASKS.md)**; thin UI line items live in **[`thin-ui-feature-completion.md`](thin-ui-feature-completion.md)**. **UniversalSurfaceXD** owns **[USXD v4 — lab + interchange](https://github.com/fredporter/UniversalSurfaceXD/blob/main/docs/roadmap-v4.md)** (surface JSON, not server runtime).

**Legacy filename:** [`UHOME-DEV-ROADMAP.md`](UHOME-DEV-ROADMAP.md) redirects here for bookmarks.

---

## How v4 is split across repos

| Layer | Repository | Role |
| --- | --- | --- |
| **Runtime** (LAN server, thin UI, Matter, host) | **uHomeNest** | Household media, kiosk/thin surfaces, contracts |
| **Surface language + UX lab** | **UniversalSurfaceXD** | JSON interchange, browser mockup — **not** production uHOME |

v4 **does not** use uDOS **#binder / Workspace** as operator UX. Thin reading is **Markdown + Tailwind Prose** (see [`contributor-dev-brief.md`](contributor-dev-brief.md)). **`sync_records`** `binder_*` fields remain for optional **`integrated-udos`** envelopes only.

---

## Planning model

- **Default:** this roadmap + **GitHub issues** + family round notes (`uDOS-dev`); no binder compile path as a uHOME **product** requirement.
- **Thin operator surfaces:** `GET /api/runtime/thin/read`, `/thin/browse`, `/thin/automation` — see [`QUICKSTART.md`](../QUICKSTART.md) for port and URLs.

---

## Vision

**uHOME Server** as the canonical **Linux-side** home-profile runtime: **Sonic-installable**, **LAN-native**, resilient across **multiple nodes**, aggregating a **household media library** from many drives and cooperating machines.

### Product shape

| Area | Intent |
| --- | --- |
| **Core** | Linux-hosted API, Jellyfin-backed media, DVR/scheduling, HA bridge, Steam-console + thin-GUI presentation |
| **Network** | One or more active servers on the LAN; satellite Steam hosts; library composed from visible storage members |
| **Clients** | Android / Google TV / Apple TV / direct-display Linux — **downstream** of server contracts (not embedded in this repo) |

---

## Current baseline (uHomeNest **3.9.x**)

- Monorepo: **`server/`**, **`matter/`**, **`host/`**, **`src/uhome_server/`**, shared `docs/`.
- HA bridge, presentation service, decentralized node/storage registries, library catalog, launcher, Sonic bundle/preflight/install-plan, dashboard routes — see [`ui/UHOME-DASHBOARD.md`](ui/UHOME-DASHBOARD.md).

### Known limitations

- Registries are **file-backed**, not full orchestration; no election/failover model yet.
- No rich distributed library **replication** layer yet.
- No **packaged** production deployment product yet; no **in-repo** rich client UI (thin lane is server-rendered prose + USXD handoff).

---

## Delivery tracks (status)

Historical “Phase 1–6” milestones are folded into these **tracks** for v4 planning.

| Track | Focus | Status |
| --- | --- | --- |
| **Runtime hardening** | CI, deps, config contracts, health checks for integrations | Ongoing |
| **Media & jobs** | DVR durability, job queue, Jellyfin hardening, library path model | In progress (see [`thin-ui-feature-completion.md`](thin-ui-feature-completion.md)) |
| **Decentralized LAN** | Node/storage topology, partial availability | Largely in place; keep hardening |
| **Sonic & host profiles** | Bundle contracts, standalone + dual-boot profiles | Largely in place |
| **Living-room & clients** | Stable API contracts for remote clients, launcher/session semantics | **Active** |
| **Operational maturity** | Runbooks, backup/restore, observability, deployment guide | Largely in place; optional future: registry publishing automation |
| **uDOS-family compatibility** | Ecosystem spine integration, contracts, and compatibility layer | In progress |
| **udev framework** | Device policies, rules, and automation | In progress |

---

## Near-term engineering backlog

- Extract and clarify playback routes vs HA command-handler scaffolding where useful.
- Broaden node authority states beyond current primary handoff.
- Storage volume **identity** rules beyond mount paths.
- Deeper Jellyfin integration tests and configuration docs.
- Stable **API contract** documentation for TV/mobile clients (align with [`clients/INTEGRATION-GUIDE.md`](clients/INTEGRATION-GUIDE.md)).
- Integrate uDOS-family compatibility layer and contracts.
- Implement udev framework policies and device management.
- Finalize sonic-installer integration and bundle creation.

---

## Cross-cutting rules

- Linux remains the **authoritative** server runtime; Windows is auxiliary in dual-boot.
- **Local-first**; degrade gracefully when nodes or storage disappear.
- **Thin HTML** stays **prose Markdown** unless a future scope explicitly adds a richer UI layer.
- **USXD** for layout handoff: [`surface-uhome-thin-kiosk.json`](https://github.com/fredporter/UniversalSurfaceXD/blob/main/interchange/examples/surface-uhome-thin-kiosk.json), composer **`?sample=uhomeThin`**.
- **uDOS-family compatibility** for ecosystem spine integration.
- **udev framework** for device policies and automation.

---

## Reference docs (governance)

| Doc | Role |
| --- | --- |
| [`contributor-dev-brief.md`](contributor-dev-brief.md) | Contributor workflow (optional `#binder` parity) |
| [`education-dev-brief.md`](education-dev-brief.md) | Education / course structure |
| [`architecture/UHOME-SERVER-DEV-PLAN.md`](architecture/UHOME-SERVER-DEV-PLAN.md) | Short v4 dev entry + links |
| [`thin-ui-feature-completion.md`](thin-ui-feature-completion.md) | Thin UI + product checklist |
| [`ui/UHOME-DASHBOARD.md`](ui/UHOME-DASHBOARD.md) | Dashboard / client API expectations |
| [USXD — uHOME handoff](https://github.com/fredporter/UniversalSurfaceXD/blob/main/docs/uhome/README.md) | Interchange authoring |
| [`installer/README.md`](installer/README.md) | sonic-installer framework and udev policies |
| [`contracts/README.md`](contracts/README.md) | uDOS-family compatibility and contracts |

---

## Version tags

- **uHomeNest product line:** root [`VERSION`](../VERSION) (**3.9.x**).
- **Python `uhome-server`:** `pyproject.toml` (semver independent of product line).

---

## Retired material

Pre-v4 phase milestone docs, migration snapshots, and tracked **`@dev/`** trees were removed in **2026-04**. Optional local copies: **`.compost/cleanup-2026-04-10/`**. See [`../dev/COMPOST-LEGACY.md`](../dev/COMPOST-LEGACY.md).
