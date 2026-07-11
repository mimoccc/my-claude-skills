---
name: task-journal
description: Use at the START of handling ANY user prompt that contains a task or assignment (including tasks added mid-turn), and whenever starting/finishing work on something. Persist the task to the memory task journal BEFORE executing it, so a crashed IDE/session loses nothing. Also check the journal at session start for unfinished work.
---

# Task journal — persist tasks before doing them

The user's IDE/session can die mid-work. Every task must survive that.

## Journal location

`<memory dir>/task-journal.md` — the per-project memory directory given in the
system prompt (for psippr: `~/.claude/projects/-home-mimo-Plocha-psippr/memory/`).
The journal is indexed from `MEMORY.md` so it loads every session.

## Rules

1. **On receiving a task prompt** (new message OR a mid-turn addition): FIRST
   append one line to `## Fronta` in the journal — `- [ ] YYYY-MM-DD <stručné
   zadání vlastními slovy, česky>` — THEN start working. No exceptions for
   "quick" tasks; those are lost the same as big ones.
2. **When starting work** on an item, mark it `- [>]` (in progress). If work
   spans steps (analysis → fix → build → commit), optionally note the current
   step after an em-dash so a crash resumes mid-task, e.g.
   `- [>] 2026-07-11 mute v lobby — fix hotový, zbývá build+commit`.
3. **When done** (built + committed), change to `- [x]` and append the commit
   hash. Move nothing; completed items stay until cleanup.
4. **Cleanup**: when `## Hotovo dnes` grows past ~15 items, delete the oldest
   completed ones — the git history already records them.
5. **At session start**: if the journal has `[ ]` or `[>]` items, surface them
   to the user before doing anything else ("z minula zbývá: …") and continue
   or ask.
6. The journal complements (not replaces) the harness TaskCreate/TaskUpdate
   tools — those die with the session; the journal is the persistent copy.

## Format

```markdown
## Fronta
- [ ] 2026-07-11 příklad čekajícího úkolu
- [>] 2026-07-11 příklad rozdělaného — krok kde to je

## Hotovo dnes
- [x] 2026-07-11 příklad hotového (abc1234)
```
