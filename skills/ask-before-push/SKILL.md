---
name: ask-before-push
description: Use before ANY git push, in any repo. The user must ALWAYS be asked for confirmation before pushing, even in automode. Single exception - the sync-skills push to mimoccc/my-claude-skills goes without asking.
---

# Always ask before push

1. **Never `git push` without asking first.** Before every push — any repo, any
   branch — ask the user for explicit confirmation (AskUserQuestion or a direct
   question). This applies even in automode / autonomous work.
2. **Commits are not gated.** Committing locally per step stays autonomous as
   before; only the push itself needs consent.
3. **One ask per push moment.** If several commits are ready, one confirmation
   covers pushing them together; don't ask per commit.
4. **Standing exception:** the skills sync to `mimoccc/my-claude-skills`
   (see the `sync-skills` skill) pushes WITHOUT asking — the user explicitly
   authorized that flow permanently.
5. If the user says "pushni" / "a pushni to" in their message, that IS the
   consent for that push — don't ask again.
