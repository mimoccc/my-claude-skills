---
name: save-test-report
description: Use in ANY project whenever the user asks for a test report ("vypis report pro testovani", "uloz report", "report na test", "save the report") or after finishing a batch of changes that the user will test by hand. Write the report as a markdown file named test-<YYYY-MM-DD_HH-MM>.md in the project root, not only into the chat answer.
---

# Test report goes into a file

The user tests by hand, often later and on another device — a report that lives
only in the chat is gone by then. Every requested report is therefore written to
disk as well.

## The rule

1. **Trigger:** the user says "ulož report" / "vypiš report pro testování" /
   "report na test" (or any wording asking for a testing report). Standing
   request from 5. 8. 2026: **always** save it after such a prompt.
2. **File:** `test-<YYYY-MM-DD_HH-MM>.md` in the **project root**, timestamp
   from the actual system clock (`date +"%Y-%m-%d_%H-%M"`), never guessed.
   Never overwrite an older report — a new prompt means a new file.
3. **Content:** what was built and installed (version + install time), one
   section per change with **what to try** and **what must happen**, plus a
   final section listing what is NOT done / still queued, so the user does not
   test something that was never delivered.
4. **Language:** the language the user speaks in the session (Czech in psippr).
5. **Answer:** keep the chat answer short and point to the file; do not paste
   the whole report twice (see `answer-minimal`).
6. **Commit:** the report file is part of the repo — commit it with the work
   (short English title, see `commit-style`).

## Why

- The user installs the build and tests hours later, sometimes on a phone with
  no access to the session; the checklist must be openable from the repo.
- Written reports also document which build a bug was reported against.

## How to apply

- Build/install first, then take the timestamp, then write the file.
- Every user-visible change from the batch gets its own bullet; behaviour that
  changed for the user (new restrictions, moved buttons) is stated explicitly,
  including when it also restricts the user themselves.
- Anything queued/blocked goes into the last section verbatim, with the reason.
