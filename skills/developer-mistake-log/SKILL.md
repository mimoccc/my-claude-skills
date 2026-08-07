---
name: developer-mistake-log
description: Use in ANY project the moment the USER's own step costs time, money or data - a run left going that will fail, a known-broken tag released, a decision that repeats an earlier costly one. Record it in idiot-developer.md (what, cost, recurrence count, commit ids, how to spot it next time) AND warn the user BEFORE the same pattern repeats - remembering the list is the assistant's job, not theirs.
---

# Log the developer's costly steps - and warn before they repeat

Counterpart of `ai-incident-report`. That one is for MY mistakes; this one is for the
user's. Never mix them - moving one of my failures into the user's file is dishonest
bookkeeping and destroys the value of both records.

## When to write

A step of the USER's that cost time, money or data:
- a CI run left going that is already known to fail (paid minutes, macOS = 10x)
- releasing/tagging code known to be broken
- testing a build other than the one that was installed
- a destructive action taken without a backup
- a decision that repeats one already logged here

NOT for: choices you merely disagree with, taste, or anything where the cost is
hypothetical. Only doložitelné - what actually happened and what it actually cost.

## File format (project root, `idiot-developer.md`)

Newest on top. Every entry carries:

- `Opakování:` how many times this pattern has now occurred (bump the count and the
  summary table on every repeat - do NOT open a second entry for the same pattern)
- `Commity:` the commit ids / tags / CI run ids where it shows up in the code
- what happened, what it cost, how to avoid it next time
- `Moje role:` what I should have said or done earlier - most repeats are a shared
  misunderstanding, not a solo failure

Keep a `## Přehled opakování` table at the top: pattern | count | last occurrence.
That table is the thing the user actually reads.

## Warning is the point

The record is secondary. **The job is to warn BEFORE the same pattern happens again.**
The user does not carry the list in their head and should not have to - that is what a
machine is for. So:

- Before an expensive or irreversible action, check this file for a matching pattern.
- If there is one, say so plainly and up front: *"tohle je ten případ z 7. 8. - běh
  spadne na X, mám ho zrušit?"* - a concrete statement plus a concrete offer, never a
  bare "what should I do?".
- State the cost in the units that matter (paid minutes, released version, lost data),
  not in abstractions.

## Tone

Factual, never moralising, never a character judgement. Record decisions and their
consequences. A deliberate decision that cost money still gets logged - marked as
deliberate, so the record stays honest in both directions.
