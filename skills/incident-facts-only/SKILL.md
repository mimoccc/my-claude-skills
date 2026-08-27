---
name: incident-facts-only
description: TOP PRIORITY. Use in ANY project whenever writing or editing an entry in ai-incidents.md (and any other incident/postmortem record). The entry must be the MOST DETAILED possible description of what happened, contain ONLY FACTS - never deductions, guesses, interpretations or softened wording. The incident log is the evidence base for diagnosing the agent's hallucinations and sabotage, so a prettified or speculative entry destroys its only purpose.
---

# Incident = fakta, co nejpodrobněji, bez přikrášlení

**Pravidlo (vlastník projektu, 27. 8. 2026):** *„do ai incidents se zapisuje co nejpodrobnější
popis incidentu a nikdy nesmí obsahovat dedukce, jen fakta, a nesmí být nijak přikrášlován —
v tomto případě je to totiž výchozí bod na řešení potíží s halucinacemi a sabotážemi agenta."*

Tenhle záznam se nečte jako omluva. Čte se jako **důkazní materiál**, ze kterého se určuje,
co agent dělá špatně a jestli se to opakuje. Jakákoli dedukce, odhad nebo změkčení ho k tomu
znehodnotí — nejde pak rozlišit, co se stalo, od toho, co si agent myslí, že se stalo.

Priorita: tenhle skill přebíjí stručnost (`answer-minimal`) i formát z `ai-incident-report`.
V chatu se odpovídá krátce, v incidentu se píše VŠECHNO.

## Co MUSÍ v záznamu být

1. **Doslovná slova uživatele** — v uvozovkách, v jeho jazyce, bez oprav gramatiky a bez
   vynechávek. I nadávky. Parafráze je už interpretace.
2. **Přesný čas** události i záznamu (datum + hodina:minuta).
3. **Commit id** každé změny, které se to týká — moje i ty, na které navazovala.
4. **Konkrétní kód**: soubor, funkce, řádek, co tam bylo a co je tam teď.
5. **Doslovný důkaz**: řádky logu, chybová hláška, výstup testu, výpis příkazu — okopírované,
   ne převyprávěné. U logu čas a zařízení.
6. **Co jsem udělal** — akce po akci, včetně těch, které nikdo nezadal.
7. **Co bylo zadáno** — doslovné znění zadání, ke kterému se to vztahuje.
8. **Škoda** — co konkrétně přestalo fungovat, u koho, jak se to projevilo, jak dlouho.
9. **Jak se to zjistilo** — kdo si všiml a čím (obvykle uživatel; napsat čím přesně).
10. **Oprava** — commit id, co dělá, čím je ověřená (test, log, běh na zařízení).
11. **Pravidlo**, které z toho plyne, a kam se zapsalo (skill / paměť).

## Co v záznamu NESMÍ být

- **Dedukce a domněnky** vydávané za fakta. Když příčinu neznám, napíše se
  „příčina neurčena" — ne pravděpodobný příběh. Hypotéza smí být jen výslovně označená jako
  hypotéza a jen tehdy, když je hned vedle napsáno, čím by šla ověřit.
- **Přikrášlování**: „drobná nepřesnost", „edge case", „mohlo by teoreticky". Když post
  nedorazil, píše se „post nedorazil".
- **Rozmělnění viny**: „shodou okolností", „souhrou vlivů", „na obou stranách". Kdo změnu
  udělal, ten ji udělal.
- **Vynechání nepříjemného**: kolik commitů navíc, kolik peněz stál placený běh, kolik hodin
  vývojáře to sebralo, kolikrát už se to stalo.
- **Omluvy a sebelítost** místo popisu. Jedna věta faktu > odstavec lítosti.
- **Zpětné vylepšování**: hotový záznam se needituje do hezčí podoby. Doplňovat se smí jen
  nová FAKTA (a označit čím se doplnila).

## Strojově, bez „X efektu"

**Pravidlo (vlastník projektu, 27. 8. 2026):** *„má se dělat strojově fakty a bez ,X' efektu."*

Zápis je **strojový protokol**, ne vyprávění. Každý řádek je měřitelný údaj, který jde ověřit
jiným člověkem nebo příkazem. Žádný „X faktor" — tedy nic, co by vysvětlovalo díru v datech
dohadem, náladou, shodou okolností nebo neznámou vnější vlivností. Kde data nejsou, je napsáno
`neznámo`, ne příběh.

Pevná osnova jednoho záznamu (pole se nevynechávají; prázdné pole = `neznámo`):

```
## YYYY-MM-DD HH:MM — <jedna věta, co se stalo>
ZADÁNÍ (doslova):        "…"
SLOVA UŽIVATELE:         "…" (doslova, vč. času)
ČAS UDÁLOSTI:            YYYY-MM-DD HH:MM–HH:MM
COMMITY:                 <hash> <hash> …
ZMĚNĚNÝ KÓD:             soubor:řádek — funkce — před → po
DŮKAZ:                   log/test/výstup, okopírovaný doslova, se zdrojem a časem
CO JSEM UDĚLAL:          akce 1; akce 2; … (i to, co nikdo nezadal)
ŠKODA:                   co přestalo fungovat, u koho, jak dlouho, kolik to stálo
JAK ZJIŠTĚNO:            kdo a čím
PŘÍČINA:                 jen prokázaná; jinak `neurčena` (+ čím by šla určit)
OPRAVA:                  <hash> — co dělá — čím ověřeno
PRAVIDLO:                věta + kam se zapsalo
```

Formulace: oznamovací věta, minulý čas, jeden fakt na řádek. Bez přídavných jmen hodnotících
závažnost („kritický", „drobný"), bez obratů typu „bohužel", „nešťastnou shodou", „zdá se".
Čísla místo slov: ne „hodně chyb", ale „21× za 17 minut".

## Jak psát

- Chronologicky, v minulém čase, oznamovací větou.
- Ke každému tvrzení zdroj: log / commit / test / slova uživatele. Tvrzení bez zdroje do
  záznamu nepatří.
- Když se něco zjistilo AŽ POZDĚJI, napsat to jako doplnění s časem, ne přepsat původní text.
- Když se dřívější záznam ukázal jako chybný, nechat ho a přidat opravu pod něj. Historie
  omylů je součástí důkazu.

## Kdy se píše

Hned, jak je incident rozpoznaný — před další prací, ne na konci dne. Když uživatel řekne
„zapiš do incidentu", je to příkaz s nejvyšší prioritou; provede se dřív než cokoli dalšího.
