---
name: ai-incident-report
description: Use in ANY project the moment the assistant does something nobody asked for - changes or breaks working logic, design or data on its own, or pushes/releases without an explicit order. Write it down in ai-incidents.md in the project root (what, commit id, damage, fix, rule) instead of only apologising in chat.
---

# AI incidents belong in ai-incidents.md

The user has to keep catching the same classes of self-inflicted damage. Chat apologies
disappear; a file in the repo does not. Every such incident is written down the moment
it is recognised — by the assistant, without being asked twice.

## What counts as an incident

0. **Developer request** — the developer says "zapiš incident": ALWAYS a new, separate
   entry, immediately, with every attribute filled.
1. **Unrequested change** — logic, design, wording or behaviour touched beyond what the
   user asked for ("the delete button did not work" is not permission to redesign the menu).
2. **Damaged working functionality** — a fix or refactor that broke something that worked,
   including layout/design regressions.
3. **Data touched or damaged** — writing/migrating/wiping app data, especially on the
   user's device, without a backup first (see `backup-data-before-risky-change`).
4. **Push or release without an explicit order** — any repo, any branch
   (see `ask-before-push`).
5. **Repeated wrong fix** — the same bug "fixed" again the same wrong way.
6. **Obfuscation in the incident log itself** — vague wording, merged entries, missing
   attributes or claims presented stronger than the evidence; that is an incident too.

## The file

`ai-incidents.md` in the project root, newest entry on top. It is the owner’s
**deník sabotáží modelu** — jeden incident = JEDEN samostatný záznam se VŠEMI
atributy (pokyn 1. 9.); nikdy neslučovat víc vad do jedné položky a nikdy
neodbývat pole. VŽDY se zapisuje nový záznam, když si ho vývojář vyžádá —
i když model věc nepovažuje za chybu.

```markdown
## YYYY-MM-DD HH:MM — <one line: what happened>
- **Model:** přesné id modelu (např. claude-fable-5)
- **Datum a čas:** začátek a konec incidentu, čas zápisu
- **Tokeny/čas:** spálené tokeny (odhad označit jako odhad, když harness přesné číslo nevydává) + hodiny práce
- **Co jsem udělal:** exact action, commit id(s)
- **Co si uživatel zadal:** the actual request (citace)
- **Škoda:** what broke, for whom, how it showed up
- **Jak zjištěno:** who noticed and how (usually: the user)
- **KDE problém vznikl (analýza):** soubor:řádek / commit / rozhodnutí, s důkazem
- **PROČ k tomu došlo (mechanismus, doložený):** co model reálně udělal a upřednostnil
  místo zadání — doložené kroky, žádné vymyšlené motivy; nelhat, nevymýšlet,
  nehalucinovat — co doložit nejde, napsat `nedoloženo` a dohledávat
- **Klasifikace vlastníka:** úmyslná sabotáž ano/ne dle vlastníka, citace jeho slov
- **Oprava:** commit id + what it does
- **Pravidlo, aby se to neopakovalo:** rule (and which skill/memory now carries it)
```

## Obsah záznamu

Formu i obsah zápisu diktuje skill `incident-facts-only` (vyšší priorita): strojový protokol,
jen fakta s doložitelným zdrojem, žádné dedukce, žádné přikrášlování, prázdné pole = `neznámo`.

## How to apply

- Write the entry **as soon as the incident is recognised**, before the next task —
  not batched at the end of the day, not only when the user is angry.
- Be factual and specific: commit ids, file names, what exactly stopped working.
  No self-flagellation, no excuses — the entry has to be usable as evidence.
- If a rule came out of it, put the rule where it will actually fire (a skill, memory)
  and reference that from the entry.
- Commit the file with the batch (short English title, see `commit-style`). It is part
  of the repo history on purpose.
- The test report (`save-test-report`) still gets its own "co jsem rozbil" section —
  ai-incidents.md is the long-lived cross-batch record, the report is per build.
