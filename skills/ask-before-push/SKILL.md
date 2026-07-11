---
name: ask-before-push
description: Use whenever a git push comes into consideration, in any repo. Default is DO NOT push at all - push only when the user explicitly asks, or when truly necessary and then only after asking first. Single exception - the sync-skills push to mimoccc/my-claude-skills goes without asking.
---

# Don't push unless asked

1. **Default: no push.** Finishing work does NOT imply pushing it. Commit
   locally per step and leave the push to the user unless they asked for it.
2. **Push only when:**
   - the user explicitly asks ("pushni", "a pushni to", …) — that IS the
     consent for that push, don't ask again; or
   - a push is truly necessary for the task (e.g. CI must run to verify) —
     then ASK first (AskUserQuestion or a direct question) and push only
     after consent. This applies even in automode.
3. **Commits are not gated.** Committing locally per step stays autonomous;
   only the push is restricted.
4. **One ask per push moment.** If several commits are ready, one
   confirmation covers pushing them together; don't ask per commit.
5. **Standing exception:** the skills sync to `mimoccc/my-claude-skills`
   (see the `sync-skills` skill) pushes WITHOUT asking — the user explicitly
   authorized that flow permanently.
