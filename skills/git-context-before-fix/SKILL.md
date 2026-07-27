---
name: git-context-before-fix
description: Use in ANY repo BEFORE fixing a reported bug or changing existing behavior. Look into git history first - find the commits that introduced/last touched the behavior, what the intent was, and whether this is a regression, a never-implemented case, or works-as-designed. Diagnose from history, not from assumptions.
---

# Git context before any fix

Before touching code to fix a reported bug, ALWAYS establish the git context
first. The user's time is expensive; a fix based on a wrong assumption about
"what used to work" wastes it twice.

## Steps (do them, don't skip)

1. **Locate the code path** for the reported behavior (grep the screen/function).
2. **History of that code**, not just the file:
   - `git log --oneline -S "<symbol>" -- <file>` — commits that touched the symbol
   - `git log -L <start>,<end>:<file>` — evolution of the exact block
   - `git show <sha>` — read the diff AND the commit title to recover intent
3. **Classify the finding** before writing any code:
   - **Regression** — it worked at commit X, broke at commit Y → fix must restore
     X's behavior; also check WHY Y changed it (don't reintroduce Y's bug).
   - **Never implemented** — the reported case was always a deliberate fallback /
     TODO → say so honestly, implement the missing case.
   - **Works as designed** — behavior matches an explicit earlier decision →
     surface the original decision to the user before changing it.
4. **Check releases**: is the relevant commit in the version the user actually
   runs (`git tag --contains <sha>`, journal/device state)? A "bug" may just be
   an unreleased fix.
5. **Report the classification to the user** in one or two sentences as part of
   the fix summary (which commit, when, regression vs gap), so they know whether
   something they paid for got broken or was never there.

## Related repo rules

- After a returned "fix", grep ALL writers/paths of the state, not the same one
  again (memory: repeated-bug-report-find-all-paths).
- Fix must not silently change other call sites' behavior — check every caller
  of the block you edit.
