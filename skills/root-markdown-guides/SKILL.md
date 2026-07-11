---
name: root-markdown-guides
description: Use whenever a feature, integration, or workflow needs setup steps, credentials, pairing, dashboard configuration, or anything a human must do manually — write/refresh a markdown guide in the PROJECT ROOT (<topic>.md). Also use when the user asks for "navod"/guide for something that exists in the repo.
---

# Markdown guides in the project root

Anything in the project that needs **manual human steps** (secrets, pairing,
dashboard clicks, external accounts, device setup) gets a guide as
`<topic>.md` in the **project root** — not buried in docs/, not only in code
comments. Examples in psippr: `whatsapp.md`, `stripe.md`.

## When to write/update one

- Adding a feature that needs setup (API keys, tokens, QR pairing, DNS
  records, dashboard configuration) → write the guide in the same commit.
- The user asks for a guide ("udelej navod / md") for an existing area →
  extract the truth from the code (never invent), document what exists.
- Changing behavior an existing guide describes → update the guide in the
  same commit; a stale guide is worse than none.

## Format rules

- Czech language (matches project comments), filename lowercase `<topic>.md`.
- Start with 2–4 sentences: what it is and how it works overall — then
  numbered setup steps with exact commands (`gh secret set …`, paths, URLs).
- Tables for file/secret/constant listings; fenced blocks for commands and
  config samples.
- Include a troubleshooting section ("když to nefunguje") with the observable
  error and the fix.
- Reference real paths in the repo (workflow files, source files, props) so
  the guide doubles as a map.
- Never put actual secret values into the guide — only names and where to
  set them.
