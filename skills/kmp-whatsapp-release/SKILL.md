---
name: kmp-whatsapp-release
description: Use when setting up a new KMP project or adding release automation to one. Every KMP project gets the WhatsApp release channel by default - a workflow that posts published release files (minus debug APK) to a WhatsApp group, plus the pairing script, its IDE run action, and the whatsapp.md guide.
---

# WhatsApp release channel — default for KMP projects

Every KMP project gets this channel prepared (it stays dormant until the user
pairs — without secrets the workflow silently skips). Copy the four pieces
from psippr and adjust names:

| Piece | Path (psippr reference) |
| --- | --- |
| Bot script (pair/groups/send, Baileys) | `scripts/whatsapp-release/send.js` + `package.json` |
| One-shot pairing script (portable Node + gh secrets) | `scripts/whatsapp-pair.sh` |
| Workflow on `release: published` | `.github/workflows/whatsapp.yml` |
| IDE run action (terminal!) | `.run/whatsappPair.run.xml` |
| Guide in project root | `whatsapp.md` |

## Invariants

- The bot MUST negotiate the current WA Web version via
  `fetchLatestBaileysVersion()` and pass it to `makeWASocket({ version, … })` —
  with the version baked into the Baileys release the server refuses
  registration ("Connection Failure") before the QR ever shows.

- Trigger is `release: published` — chains onto whatever publishes GitHub
  Releases in that project.
- **Debug APK is always excluded** (`rm -fv assets/*-debug.apk`).
- Session lives in Actions cache (`whatsapp-session-*`, saved with
  `if: always()`), secret `WA_SESSION_B64` is only the first-run/fallback
  copy; group target is secret `WA_GROUP_JID`.
- Missing secrets → the job gates itself off and succeeds (safe on forks and
  before pairing).
- `.gitignore` must cover `scripts/whatsapp-release/session/`, `session.b64`,
  `node_modules/` — the session IS the WhatsApp login.
- The pairing run action must run **in terminal** (`EXECUTE_IN_TERMINAL`)
  — the QR code renders in the console.
- Baileys is an unofficial client (ToS risk) — recommend a dedicated number,
  never silently pair anything.

## Setup for the user

One command: `./scripts/whatsapp-pair.sh` (or the `whatsappPair` run action) —
downloads portable Node if missing, shows QR, lists groups, sets both GitHub
secrets via `gh`. Document it in the project's `whatsapp.md` (see
root-markdown-guides skill).
