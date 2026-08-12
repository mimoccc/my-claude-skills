---
name: ai-incident-report
description: Use in ANY project the moment the assistant does something nobody asked for - changes or breaks working logic, design or data on its own, or pushes/releases without an explicit order. Write it down in ai-incidents.md in the project root (what, commit id, damage, fix, rule) instead of only apologising in chat.
---

# AI incidents belong in ai-incidents.md

The user has to keep catching the same classes of self-inflicted damage. Chat apologies
disappear; a file in the repo does not. Every such incident is written down the moment
it is recognised — by the assistant, without being asked twice.

## What counts as an incident

1. **Unrequested change** — logic, design, wording or behaviour touched beyond what the
   user asked for ("the delete button did not work" is not permission to redesign the menu).
2. **Damaged working functionality** — a fix or refactor that broke something that worked,
   including layout/design regressions.
3. **Data touched or damaged** — writing/migrating/wiping app data, especially on the
   user's device, without a backup first (see `backup-data-before-risky-change`).
4. **Push or release without an explicit order** — any repo, any branch
   (see `ask-before-push`).
5. **Repeated wrong fix** — the same bug "fixed" again the same wrong way.

## The file

`ai-incidents.md` in the project root, newest entry on top:

```markdown
## YYYY-MM-DD HH:MM — <one line: what happened>
- **Co jsem udělal:** exact action, commit id(s)
- **Co si uživatel zadal:** the actual request
- **Škoda:** what broke, for whom, how it showed up
- **Jak zjištěno:** who noticed and how (usually: the user)
- **Oprava:** commit id + what it does
- **Pravidlo, aby se to neopakovalo:** rule (and which skill/memory now carries it)
```

## How to apply

- Write the entry **as soon as the incident is recognised**, before the next task —
  not batched at the end of the day, not only when the user is angry.
- Be factual and specific: commit ids, file names, what exactly stopped working.
  No self-flagellation, no excuses — the entry has to be usable as evidence.
- If a rule came out of it, put the rule where it will actually fire (a skill, memory)
  and reference that from the entry.
- Commit the file with the batch (short English title, see `commit-style`). It is part
  of the repo history on purpose.
- The test report (`save-test-report`) still gets its own "co jsem rozbil" section —
  ai-incidents.md is the long-lived cross-batch record, the report is per build.
