---
name: agent-edit-lint
description: Use whenever a subagent (or you) edits source files in ANY project - after EVERY edited file, lint it and remove imports that the edit left unused. Applies to all fan-out/parallel agent work, not just Kotlin. Prevents unused-import noise and duplicate-facade/compile errors from landing in the user's repo.
---

# Po každé editaci: lint + úklid importů

Agent, který soubor upravil, za sebou **musí uklidit**. Uživatel nechce v repu
nepořádek po automatické editaci — nefunkční nebo zbytečné řádky se počítají
jako poškození souboru.

## Pravidlo

Pro **KAŽDÝ** soubor, který agent upravil nebo vytvořil:

1. **Odstranit nepoužité importy** — jak ty, které agent přidal a nakonec
   nevyužil, tak ty, které jeho úpravou přestaly být potřeba (např. přesunul
   nebo nahradil kód, který import používal).
2. **Zkontrolovat, že přidané importy skutečně existují a jsou použité** —
   přidaný import bez použití je stejná chyba jako chybějící import.
3. **Prolinovat soubor** projektovým linterem, pokud existuje
   (ktlint, detekt, eslint, ruff, gofmt…). Když je linter v projektu jen
   reportovací (nebrání buildu), stejně nesmí agentova editace přidat NOVÁ
   hlášení — stará se neopravují (to je samostatné zadání).

## Ověření na konci

Agent na konci své práce projde seznam souborů, které sáhl, a u každého ověří
body výše. V reportu uvede, co uklidil. „Přidal jsem preview" bez kontroly
importů není hotová práce.

Když má agent zakázáno spouštět build (typicky při paralelním fan-outu, kde by
si agenti navzájem shazovali kompilaci), kontrola importů se dělá **čtením
souboru** — každý import se musí dát najít v těle souboru. Zodpovědnost za
finální kompilaci pak nese ten, kdo agenty pustil.

## Proč

- Nepoužitý import je mrtvý kód, který uživatel musí ručně mazat před commitem.
- V Kotlin/KMP navíc hrozí tvrdá chyba: přidání běžné funkce do souboru, kde
  byla jen `expect` deklarace, vyrobí JVM facade třídu kolidující se
  stejnojmenným souborem z platformní source sady
  („Duplicate JVM class name … Kt"). Náhled/pomocnou funkci proto v takovém
  případě dát do VLASTNÍHO souboru.
- Uživatel si commituje sám a nechce v diffu řádky, které tam nepatří.
