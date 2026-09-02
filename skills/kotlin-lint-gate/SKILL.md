---
name: kotlin-lint-gate
description: MANDATORY gate after EVERY batch of Kotlin/KMP edits in ANY project, BEFORE saying done, before commit, and always before push. Two layers - (1) run check_kt_imports.py from this skill dir on every edited .kt file (catches missing annotation imports and unused imports in under a second), (2) compile every target this host can build for the affected modules. Created 2.9.2026 after TWO paid macOS release runs died on errors a local lint/compile would have caught instantly.
---

# Kotlin lint gate — brána, ne sliby

2\. 9. 2026: dva placené macOS release runy (v1.0.197, v1.0.198) spadly na chybách,
které by lokální lint/kompilace chytily okamžitě a zdarma (chybějící importy
`@file:` anotací po one-class-per-file splitu; `private` helpery přes soubory;
suspend mimo korutinu). Vlastník: „resime placenym pushem to, co by lint udelal
okamzite". Tahle brána je proto POVINNÁ a mechanická — neběží na paměti, ale na
příkazech níže.

## Kdy (bez výjimky)

- po KAŽDÉ dávce editací `.kt` souborů — než řeknu „hotovo",
- před KAŽDÝM commitem, který sahá na `.kt`,
- před KAŽDÝM push/release (spolu s `read-incidents-before-push`),
- zvlášť po hromadných akcích: split souborů, přesuny mezi soubory/moduly,
  přejmenování balíčků, fan-out subagentů (viz `agent-edit-lint`).

## Vrstva 1 — okamžitý skript (zlomek sekundy, vždy)

```bash
python3 <skill_dir>/check_kt_imports.py <každý editovaný .kt soubor>
```

Chytá: `@file:` anotace bez importu (`JvmName`, `ExperimentalForeignApi`, …
— přesně pád v1.0.197) a nepoužité importy. Nález = opravit HNED, pak znovu.

## Vrstva 2 — kompilace všeho, co tenhle stroj umí (před „hotovo")

Pro každý afektovaný modul spustit VŠECHNY lokálně dostupné compile targety —
viditelnosti (`private` přes soubory), suspend chyby a typy chytí jen kompilátor:

- **psippr:** `./gradlew iosCheck` (shared+db iosArm64; FUNGUJE jen s kompletním
  klibem v `shared/prebuilt/` — když task spadne na chybějící/nekompletní klib,
  ŘÍCT to nahlas, ne tiše přeskočit) a pro ostatní moduly s iOS targetem
  `:modul:compileKotlinIosArm64` (webrtc, phone — klib webrtc je v repu) +
  `:modul:compileAndroidMain`.
- **jiný projekt:** ekvivalent — metadata + JVM/Android + každý native target,
  který na hostu jde.

## Report

Na konci odpovědi s editacemi uvést, KTERÉ brány běžely a jak dopadly
(např. „gate: check_kt_imports 19 souborů OK; :webrtc+:phone iosArm64 OK;
:shared iosArm64 z Linuxu nejde — nekompletní klib, jede až na CI").
Target, který lokálně ověřit nejde, se JMENUJE — zamlčení = mlžení.

## Proč skill a ne dobrá vůle

Pravidlo „linkuj po editaci" existovalo (`agent-edit-lint`) a nestačilo, protože
vise na tom, jestli si vzpomenu. Tahle brána je checklist s konkrétními příkazy
navázaný na okamžiky (hotovo/commit/push), které nastanou vždy. Poruší-li se,
je to porušení výslovného pokynu vlastníka z 2. 9. 2026, ne opomenutí.
