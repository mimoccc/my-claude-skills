---
name: read-incidents-before-push
description: Use in ANY project immediately before a git push (and before triggering a release/CI run that costs money). Read ai-incidents.md and idiot-developer.md first, check the pending change against every rule already written there, and fix what repeats BEFORE it leaves the machine. The incident log is worthless if it is only ever written to.
---

# Read the incident log before you push

The incident log exists so the same mistake never gets pushed twice. Writing it
down and then pushing the same class of change without re-reading it is how a
"fixed" bug comes back and costs another paid CI run.

## When

- Before EVERY `git push` of a project repo.
- Before `gh workflow run` / tagging / anything that starts a paid build.
- After `git commit` when the next step is obviously a push.

(This does not replace `ask-before-push` — that skill decides *whether* to push,
this one decides *what must be true* before the push happens.)

## What to do

1. **Read the log(s), do not skim from memory.**
   - `ai-incidents.md` — what I broke, and the rule each incident produced.
   - `idiot-developer.md` — the user's own recurring costly steps; warn them
     BEFORE they repeat one, that is my job, not theirs.
   If neither file exists in the repo, say so once and continue.

2. **Match the pending change against every rule in the log.** Go through
   `git diff origin/<branch>..HEAD --stat` and ask, for each recorded incident:
   *does this diff touch the same area, the same file, or the same class of
   mistake?* Typical repeats worth stopping for:
   - a change that only CI can verify, pushed without checking the last run of
     that same workflow,
   - a new build target / bundle id / signing input added without the manual
     side (portal, secret, key) being in place,
   - a "fix" for a bug that a previous incident says has several code paths —
     grep for all of them,
   - touching logic nobody reported as broken,
   - version/tag steps whose ordering already burned a release.

3. **Fix the repeat before pushing, not after.** If the diff repeats a logged
   mistake, that is a blocker, not a note. Fix it, or tell the user in one
   sentence what will happen and let them decide.

4. **Report before pushing.** One or two lines, e.g.
   `Incidenty přečtené: 4. Tenhle push se týká iOS podpisu (incident 2026-08-08)
   — profil pro extension pořád chybí, ipa proto poletí bez rozšíření.`
   If nothing in the log applies, say `Incidenty přečtené, nic se neopakuje.`

5. **If the push turns out to be a new incident**, write it with
   `ai-incident-report` right away — and re-read the log before the next push.

## Non-negotiables

- Never claim "checked" without actually opening the files this session.
- Never answer "is it ok?" from a different signal than the one asked about
  (a green lint run is not a green release run) — that exact substitution is
  itself a logged incident.
- The log is append-only history: fix code, not the record.
