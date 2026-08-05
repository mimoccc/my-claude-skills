---
name: divide-et-impera
description: HIGH PRIORITY working rule for ANY project and ANY task - always divide et impera. Split every assignment into small parts before doing it - small steps, small classes, small functions, small commits - and never write one big blob of code or run one big undivided step. Use whenever starting a task, designing code, planning a refactor, or when a change starts growing beyond a single small unit.
---

# Divide et impera — always split the work

Standing rule from the user (5. 8. 2026): **everything gets decomposed first.**
No task is executed as one lump, no feature is written as one giant function or
class, no refactor lands as one unreviewable change.

## The rule

1. **Split the assignment before touching code.** Write out the small steps
   (diagnose → smallest fix → build → verify → commit) and do them one by one.
   If a step cannot be described in one sentence, it is still too big.
2. **Split the code into small units.** One class = one responsibility (see
   `one-class-per-file`), one function = one job. A composable that renders a
   screen delegates to per-part composables; a state holder delegates to small
   private helpers. No 300-line functions, no god classes.
3. **Split the change into small commits.** One topic per commit
   (see `commit-style`), so a regression can be bisected to a single small step.
4. **Split verification too.** Compile/lint/install after each meaningful part
   instead of one big check at the end — a failure then points at one small
   change, not at everything.
5. **Split shared numbers and rules into one named place.** When the same value
   or rule is needed in two spots, extract it (constant, helper, enum) — a
   duplicated literal is an undivided decision that drifts apart later.
6. **When a part grows mid-work, stop and split again.** If a "small fix" is
   turning into a big diff, cut it: land the isolated part first, queue the
   rest as its own step.

## Why

- The user repeatedly gets bugs back from oversized changes: one broken corner
  case hides in a large blob, and reverting costs the whole feature.
- Small units make review, git history, bisect and targeted re-fixes cheap;
  large ones make every later fix a guess.
- Repeatedly re-broken behaviour (report button, gesture handling) always came
  from decisions living in several places at once — splitting a rule into one
  owner is the fix.

## How to apply

- **Starting a task:** first write the step list (task journal entry counts),
  then execute steps in order; report which step you are on.
- **Designing code:** name the parts before writing them (which class, which
  file, which function) — if the names do not exist yet, the split is missing.
- **During work:** whenever a file, function or diff feels big, cut it and
  continue in parts.
- **Ending a task:** each part compiled, verified and committed separately;
  anything left over goes to the queue as its own named step, never silently
  bundled in.
