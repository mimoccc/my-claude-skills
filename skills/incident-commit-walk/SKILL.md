---
name: incident-commit-walk
description: Use for EVERY incident in tool-sabotages/ai-incidents.md when the owner asks to restore or verify original functionality — walk the git history commit by commit for the affected code, write a short report per commit (what the commit changed, what the functionality was BEFORE it) and ASK the developer to confirm the original behaviour before touching anything. Owner 19. 9. 2026: "u kazdeho incidentu projit commit po commitu a zeptat se s reportem na puvodni funkcionalitu, potvrdi vyvojar, bez nej ani krok".
---

# Incident → commit po commitu → potvrzení vývojáře → teprve krok

Zadání vlastníka 19. 9. 2026 (doslova): „u kazdeho incidentu projit commit po commitu a
zeptat se s reportem na puvodni funkcionalitu, potvrdi vyvojar, bez nej ani krok".

## Postup pro jeden incident

1. **Vymezit kód** z položky incidentu (soubory, funkce, řádky, commity, které uvádí).
2. **Historie commit po commitu**:
   `git log --format='%h %ad %s' --date=format:'%Y-%m-%d %H:%M' --follow -- <soubor>`
   a pro každý commit, který se dotkl vymezeného kódu, `git show <hash> -- <soubor>`.
   Začít od prvního commitu, který funkci ZAVEDL (nebo od posledního stavu, o kterém
   vlastník řekl, že fungoval), a jít dopředu.
3. **Report ke každému commitu** (krátký, jen fakta):
   - hash, datum, titulek;
   - co commit změnil v dotčené funkci (1–3 věty, s `soubor:řádek`);
   - jak se funkce chovala PŘED commitem a PO něm (podle diffu, ne podle domněnky);
   - zda je to zadaná změna (odkaz na pokyn v ledgeru `doc/funkcionalita/` nebo v
     incidentu), nebo změna bez zadání.
4. **Otázka vývojáři** (AskUserQuestion nebo prostý dotaz): „Je tohle původní
   požadovaná funkcionalita?" — s nabídkou: potvrdit stav před commitem X / po commitu Y /
   jiný popis. **Bez potvrzení se NEMĚNÍ ANI ŘÁDEK.**
5. Po potvrzení: oprava přesně na potvrzený stav (`only-reported-scope`), test
   (`android-instrumentation-regression-test` / unit), ledger, a zápis do incidentu
   jen na pokyn (`ai-incident-report`).

## Zakázáno

- Přeskakovat commity „protože jsou zjevně nesouvisející" — do reportu patří i věta
  „commit X se dotčené funkce netýká (změnil jen Y)".
- Domýšlet původní chování z komentářů v kódu — komentáře psal tentýž model; platí diff
  a slovo vývojáře.
- Cokoli opravovat před potvrzením.
