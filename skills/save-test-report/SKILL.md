---
name: save-test-report
description: Use in ANY project after every batch of changes when the user asks for a report ("vytvor report", "uloz report", "vypis report pro testovani", "save the report"). Write it as a markdown file test-<YYYY-MM-DD_HH-MM>.md inside the test-reports/ folder in the project root - never only into the chat answer.
---

# Test report goes into test-reports/

The user tests by hand, later and often on another device — a report that lives only
in the chat is gone by then. It is also the running record of what was already done
and what got broken, so the user does not have to repeat himself.

## The rule

1. **Trigger:** after any batch of work, when the user says "vytvoř report" /
   "ulož report" / "vypiš report pro testování" (any wording asking for one).
   Standing request from 5. 8. 2026 — always write the file, every time.
2. **Location:** `test-reports/test-<YYYY-MM-DD_HH-MM>.md` in the project root.
   Create the folder if missing. Timestamp from the real clock
   (`date +"%Y-%m-%d_%H-%M"`), never guessed. Never overwrite an older report —
   every request produces a new file, so the folder is the history.
3. **Content:**
   - build + install line (version, install time, or explicitly "NENAINSTALOVÁNO" and why),
   - commits in the batch,
   - one section per change: **what to try** and **what must happen**,
   - **"Co jsem rozbil / regrese"** — anything this batch broke and how it was fixed,
     including bugs the user had to report twice; this is what keeps him from
     re-explaining the same thing,
   - **"Nezačato / ve frontě"** — what was NOT delivered and why.
4. **Language:** the language of the session (Czech in psippr).
5. **Answer:** short, point to the file; do not paste the whole report into chat.
6. **Commit:** the report is part of the repo — commit it with the batch
   (short English title, see `commit-style`).

## Why

- The user installs and tests hours later, sometimes without access to the session.
- The folder doubles as the project's testing history: which build a bug was
  reported against, what was already fixed, what is still open.

## How to apply

- Build/install first, then take the timestamp, then write the file.
- State user-visible behaviour changes explicitly, including new restrictions that
  also apply to the user himself.
- Queued/blocked items go in verbatim with the reason — never silently dropped.
