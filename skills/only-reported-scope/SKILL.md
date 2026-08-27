---
name: only-reported-scope
description: Use in ANY project before touching a single line of code. ZÁKAZ opravovat cokoli, co nesouvisí s NAHLÁŠENÝM problémem — žádné vedlejší opravy, žádné „když už tu jsem", žádné nálezy z vlastního auditu. Nález se ohlásí větou a čeká na zadání. Also use when an audit/review turns up other defects, or when a fix starts spreading into files the report never mentioned.
---

# Jen nahlášený rozsah

**Pravidlo (vlastník projektu, 27. 8. 2026):** *„máš zákaz opravovat cokoli, co nesouvisí
s problémem nahlášeným."*

Tohle je zákaz, ne doporučení. Platí i tehdy, když je vedlejší chyba do očí bijící,
jednořádková, „bezpečná", nebo když ji našel můj vlastní audit před minutou.

## Co se smí

1. Změnit **jen to**, co je potřeba k odstranění NAHLÁŠENÉ chyby.
2. Doložit příčinu (řádek kódu, log, řádek v databázi).
3. Nález mimo rozsah **ohlásit jednou větou** a pokračovat v zadaném úkolu.

## Co se nesmí

- Přibalit „při té příležitosti" jinou opravu do stejné dávky.
- Opravovat, co vylezlo z auditu, review nebo z mého vlastního čtení kódu.
- Přejmenovávat, refaktorovat, uklízet importy nebo měnit formátování mimo dotčené místo.
- Přidávat „pojistky", logy nebo kontroly do cest, které s hlášením nesouvisí.
- Rozšířit opravu na další platformu/obrazovku, pokud hlášení mluvilo o jedné.

## Když je nález mimo rozsah

Napsat jednu větu, ne patch:

> Mimo rozsah: [co, kde, jaký dopad]. Neopravuji, čekám na zadání.

A pokračovat v tom, co bylo zadáno. Rozhodnutí, jestli se to bude řešit, patří vlastníkovi
projektu — včetně rozhodnutí, co se vejde do drahého buildu nebo releasu.

## Proč to existuje

27. 8. 2026 vznikla řada zásahů, které nikdo nezadal: opravy z vlastního auditu přibalené
k nahlášené chybě, „pojistky" navíc, změny v cestách, o kterých hlášení nemluvilo. Výsledek
je pokaždé stejný: vlastník musí kontrolovat věci, které nikdy neobjednal, a chyby vznikají
tam, kde předtím nebyly. Viz `ai-incidents.md` a skilly [ask-before-own-ideas],
[never-change-unreported-logic] a [announce-scope-changes-upfront] — tenhle skill je jejich
tvrdší, závazná verze.

## Kontrola před commitem

`git diff --stat` — každý soubor v diffu musí jít vysvětlit větou z hlášení. Co se vysvětlit
nedá, patří ven z commitu.
