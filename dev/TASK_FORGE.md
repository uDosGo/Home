# Task Forge v1 — `TASKS.md` syntax (uHomeNest)

Markdown-native tasks for **`TASKS.md`**. Same family format as [UniversalSurfaceXD `docs/dev/TASK_FORGE.md`](https://github.com/fredporter/UniversalSurfaceXD/blob/main/docs/dev/TASK_FORGE.md).

## Sections

```markdown
## Backlog
## In Progress
## Blocked
## Done
```

| Section | Meaning |
| --- | --- |
| Backlog | Defined, not started |
| In Progress | Active |
| Blocked | Waiting (say why under the item) |
| Done | Recent completions — trim often |

## Task lines

**Open:** `- [ ] Title`  
**Done:** `- [x] Title`

**With ID and tags (recommended):**

```markdown
- [ ] [UHN-SRV-001] Short title #feature #server
```

**ID prefix hints:** `UHN-SRV` (server), `UHN-MAT` (matter), `UHN-HST` (host), `UHN-META` (monorepo-wide).

**Tags (max 2–3):** `#feature` `#fix` `#docs` `#infra` `#core`

## Metadata (optional)

Indented lines under a task:

```markdown
- [ ] [UHN-SRV-010] Add health probe
  ↳ Scope: `server/src/uhome_server/routes/`
  ↳ Outcome: JSON contract documented
```

---

Full spec and edge cases: **UniversalSurfaceXD** [`docs/dev/TASK_FORGE.md`](https://github.com/fredporter/UniversalSurfaceXD/blob/main/docs/dev/TASK_FORGE.md).
