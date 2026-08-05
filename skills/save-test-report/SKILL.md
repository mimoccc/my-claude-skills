---
name: save-test-report
description: Use in ANY project after every batch of changes when the user asks for a report ("vytvor report", "uloz report", "vypis report pro testovani", "save the report"). Write it as test-reports/<YYYY-MM-DD>/test-<HH-MM>.md - one folder per day, one file per batch - and put the commit id next to every item.
---

# Test report goes into test-reports/<den>/

The user tests by hand, later and often on another device — a report that lives only
in the chat is gone by then. The folder is also the running record of what was already
done, what got broken, and which commit each thing came from.

## The rule

1. **Trigger:** after any batch of work, when the user says "vytvoř report" /
   "ulož report" / "vypiš report pro testování" (any wording asking for one).
   Standing request from 5. 8. 2026 — always write the file, every time.
2. **Location:** `test-reports/<YYYY-MM-DD>/test-<HH-MM>.md` in the project root —
   **a folder per day**, a file per batch. Create folders as needed. Date and time
   from the real clock (`date +"%Y-%m-%d %H-%M"`), never guessed. Never overwrite an
   older report; the tree is the history.
3. **Commit ids everywhere.** Header lists the batch range; **every item carries the
   commit id it came from** (`… (68dcf3e6)`), including items in the
   "co jsem rozbil" section. Without ids neither side can jump back to the change.
4. **A repeated bug gets its history.** When the user reports the same thing again,
   the item must list **every previous "fix" commit id, what each one changed and why
   it did not hold**, plus the id and reasoning of the current fix. Example shape:
   `report button: 1. pokus a1b2c3d (klamp z odhadnutých čísel — nedosáhl do rohů),
   2. pokus 162787d4 (meze ze stejných konstant jako kotva — příčina byla duplicita
   čísel na dvou místech)`. Without that chain the same wrong fix comes back.
5. **Content:**
   - build + install line (version, install time, or explicitly "NENAINSTALOVÁNO" and why),
   - one section per change: **what to try** and **what must happen** + commit id,
   - **"Co jsem rozbil / regrese"** — what this batch broke and how it was fixed, with
     commit ids; this is what keeps the user from re-explaining the same thing,
   - **"Nezačato / ve frontě"** — what was NOT delivered and why.
6. **Language:** the language of the session (Czech in psippr).
7. **Answer:** short, point to the file; do not paste the whole report into chat.
8. **Commit:** the report is part of the repo — commit it with the batch
   (short English title, see `commit-style`).

## Why

- The user installs and tests hours later, sometimes without access to the session.
- Daily folders keep a long session readable; commit ids make every claim checkable
  and let a regression be bisected straight from the report.

## How to apply

- Build/install first, then take date+time, then write the file.
- Get the ids from `git log --oneline` for the batch — never invent or approximate them.
- State user-visible behaviour changes explicitly, including new restrictions that
  also apply to the user himself.
- Queued/blocked items go in verbatim with the reason — never silently dropped.
