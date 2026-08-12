---
name: platform-parity
description: Use in ANY multiplatform project (KMP/CMP) whenever writing, reviewing or fixing a feature, a store, an engine or a UI screen — every platform must get the SAME capability 1:1 (Android, iOS, desktop, web). When a difference shows up during development, STOP and report it to the user instead of quietly shipping the platform that happens to work.
---

# Všechny platformy 1:1

Funkce, která existuje na jedné platformě, musí existovat na všech, které projekt
staví. Když se během vývoje najde rozdíl, **ohlásí se uživateli** — nezamlčí se
a neobejde se náhradním řešením jen na jedné straně.

## Proč

Rozdíl mezi platformami se nikdy neprojeví jako „ta funkce chybí". Projeví se
jako pád nebo jako nepochopitelné chování měsíce potom, u zákazníka, na tom
zařízení, které nikdo netestuje.

Doložený případ (psippr, 9. 8. 2026): Android a desktop měly úložiště v SQLite
s médii v souborech, **iOS měl vlastní JSON store**, který držel celou konverzaci
včetně base64 médií v jednom souboru. Každý dotaz na alba tak parsoval celý archiv
do paměti a iPhone appku zabil na 3,3 GB (`JetsamEvent`, `per-process-limit`).
Modul `db` neměl iOS targety — nikdo to neoznámil, jen se to obešlo.

## Pravidlo

1. **Než něco napíšeš:** zjisti, jestli to existuje na všech platformách. Když ne,
   ohlas to a zeptej se, jestli to doplnit hned, nebo si to zapsat.
2. **Když píšeš expect/actual:** actual musí být pro KAŽDÝ target. Prázdný stub je
   platná odpověď jen tam, kde to dává smysl (např. web jako vzdálený klient) —
   a musí být komentářem vysvětleno proč.
3. **Když najdeš rozdíl:** napiš, co je jinde, na které platformě, čím to je a co
   to znamená pro uživatele. Neschovávej to do commit message.
4. **Když rozdíl zůstává schválně:** patří do reportu a do poznámek, ne jen do hlavy.

## Na co se dívat

- **Úložiště a data**: stejný formát, stejná migrace, stejné limity.
- **Enginy a síť**: co umí jeden, musí umět druhý (viz parita jvm/iOS enginu).
- **UI**: stejná obrazovka, stejné stavy, stejné chování gest a klávesnice.
- **Build**: má modul VŠECHNY targety? U projektů s vypnutou automatickou
  hierarchií zkontroluj i zapojení zdrojových sad (`printSourceSetGraph`) —
  chybějící vazba `iosMain` znamená, že se ten kód nikdy nepřeloží.
