# Universal development — uHomeNest + UniversalSurfaceXD

**uHomeNest** and **UniversalSurfaceXD (USXD)** share **Universal Dev Notes (UDN)**: `.local/` for scratch, **`.compost/`** for replaced local copies, repo-root **`TASKS.md`** + **`dev/TASK_FORGE.md`**.

| Concern | uHomeNest | UniversalSurfaceXD |
| --- | --- | --- |
| **v4 product plan** | **[`docs/ROADMAP-V4.md`](../docs/ROADMAP-V4.md)** (canonical) | **[USXD v4 roadmap](https://github.com/fredporter/UniversalSurfaceXD/blob/main/docs/roadmap-v4.md)** |
| Product version | **uHomeNest v3.9** — root **`VERSION`** (**3.9.x**); Python **`uhome-server`** uses `pyproject.toml` | Root `package.json` **4.4.x** |
| Thin / kiosk UX implementation | `server/`, `src/uhome_server/`, `docs/ui/` | Lab + interchange only (not production runtime) |
| Surface JSON for UX handoff | Consume or reference USXD examples; see **`../UniversalSurfaceXD/docs/uhome/README.md`** | **`interchange/examples/surface-uhome-thin-kiosk.json`**, composer **`?sample=uhomeThin`** |

## Editor workspaces

| File | Loads |
| --- | --- |
| **`uHomeNest.code-workspace`** (uHomeNest repo root) | `uHomeNest` + sibling **`../UniversalSurfaceXD`** |
| **`UniversalSurfaceXD/UniversalSurfaceXD-v4.siblings.code-workspace`** | USXD + optional siblings, including **`../uHomeNest`** |

Open whichever repo you start from; both can include the other as a folder.

## Commands (typical)

**uHomeNest — server checks**

```bash
cd ~/Code/uHomeNest
bash scripts/run-uhome-server-checks.sh
```

**USXD — UX designer + validate interchange**

```bash
cd ~/Code/UniversalSurfaceXD
npm run ux-designer:dev
npm run ux:validate-surfaces
```

## Further reading

- uHomeNest: [`DEV.md`](../DEV.md), [`docs/MONOREPO.md`](../docs/MONOREPO.md), [`docs/ROADMAP-V4.md`](../docs/ROADMAP-V4.md)
- USXD: [`docs/roadmap-v4.md`](https://github.com/fredporter/UniversalSurfaceXD/blob/main/docs/roadmap-v4.md), [`interchange/README.md`](https://github.com/fredporter/UniversalSurfaceXD/blob/main/interchange/README.md)
