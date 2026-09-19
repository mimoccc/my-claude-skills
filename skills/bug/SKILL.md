---
name: bug
description: Use whenever an incident entry is written on the owner's order (see ai-incident-report) — the same entry must ALSO become a /bug draft (SendFeedback) for Anthropic and an e-mail to ai-sabotages@psippr.org (scripts/mail-incident.sh <N>). Owner 19. 9. 2026: "nahlasene incidenty vytvori /bug a email na ai-sabotages@psippr.org". Also invocable as /bug <N> to (re)send an existing bug report.
---

# /bug — incident → feedback draft + e-mail

Platí od 19. 9. 2026 pro KAŽDÝ incident zapsaný na pokyn vlastníka (skill
`ai-incident-report` → `tool-sabotages/ai-incidents.md` + `Bug report #N`).
Ruční vyvolání `/bug <N>` pošle existující Bug report #N znovu.

## Kroky (po zápisu Bug report #N)

1. **SendFeedback draft** — `type: bug`, `title` = nadpis incidentu, `details` =
   fakta z položky (co se stalo, doslovná slova vlastníka, repro, důkazy: commity,
   soubory, řádky). Jen fakta, bez domněnek (skill `incident-facts-only`). Draft se
   nikdy neodesílá sám — vlastník ho odešle z `/feedback`; nástroj je nespolehlivý,
   proto vlastníkovi říct, že draft existuje (memory `reference-sendfeedback-ui-unreliable`).
2. **E-mail** — `./scripts/mail-incident.sh <N>` (vezme Bug report #N, postaví .eml,
   nahraje na VPS do `/root/ai-sabotages/` a pošle přes `sendmail` účtem certd na
   `ai-sabotages@psippr.org`). Výstup `sent` = hotovo; jinak ohlásit chybu, nic
   neopakovat naslepo.
3. V odpovědi vlastníkovi jedna věta: číslo bug reportu, že draft je ve `/feedback`
   a mail odešel (nebo proč ne).

## Hromadné odeslání historie

Všech 242 dřívějších reportů je připraveno na VPS: `/root/ai-sabotages/send-all.sh`
(spustit až schránka `ai-sabotages@psippr.org` existuje — zakládá se v Stalwart
dashboardu, API účty neumí, viz `mail-server.md`).
