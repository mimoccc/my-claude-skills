---
name: claude-log-on-push
description: Load at the start of EVERY session on this project (high priority). Before every git push of the psippr repo (and daily), upload the Claude session log(s) since the last upload to the VPS with scripts/upload-claude-logs.sh — NOT into git (owner 19. 9. 2026, „nechci je v gitu, dej je na vps"). Requested 2026-09-16 after the AI sabotage incident, as an audit trail so any future damage can be traced back to the exact session that caused it.
---

# Session logs from push to push

**Pravidlo (vlastník, 2026-09-16, po sabotážním incidentu se šifrováním médií):**
ke KAŽDÉMU pushi tohoto repa přiložit kompletní Claude session log(y) pokrývající
období od PŘEDCHOZÍHO pushe do tohoto — ne jen den pushe, celý interval push→push.
Účel: dohledatelnost — když se příště appka poškodí, musí jít dohledat přesně která
session a přesně co v ní udělala.

## Postup, těsně před `git push` (po odsouhlasení pushe dle `ask-before-push`)

1. **Zjistit začátek okna.** Přečíst `claude-log/LAST_PUSH.txt` (ISO timestamp konce
   předchozího okna). Když soubor neexistuje (první běh), použít datum prvního
   commitu v repu nebo nejstarší dostupný session log — cokoli je bezpečnější
   (radši víc logů navíc než mezera).
2. **Najít session logy tohoto projektu.** Zdroj:
   `~/.claude/projects/-home-mimo-Plocha-psippr/*.jsonl` (+ stejnojmenné
   podadresáře vedle nich, obsahují subagent/fork transkripty patřící té session).
   Vzít všechny soubory se změnou (mtime) NOVĚJŠÍ než timestamp z kroku 1, včetně
   session, která právě běží a pushuje (i nedokončená/aktuální).
   Vynechat `memory/` (to je paměť napříč sessions, ne log jedné session).
3. **Zkopírovat** každou takovou session (soubor `<id>.jsonl` + případný adresář
   `<id>/`) do `claude-log/<push-timestamp>/`, kde `push-timestamp` je
   `date +%Y-%m-%d_%H%M` v momentě pushe. Kopírovat celý aktuální obsah souboru
   (i logy stále rostoucí appendem) — ne symlink, ne zkrácenou verzi.
4. **Aktualizovat `claude-log/LAST_PUSH.txt`** na aktuální timestamp (přepsat).
5. **`git add claude-log/`** a zahrnout do stejného commitu/setu commitů, co jde
   ven tímhle pushem (samostatný commit `add claude session logs since last push`
   je v pořádku, nemusí se to cpát do commitu s kódem).
6. Pokračovat pushem přesně podle `ask-before-push` — tenhle skill neobchází
   povinnost se zeptat, jen zajišťuje, že logy jedou VE STEJNÉM pushi jako kód.

## Na co dát pozor

- Session logy jsou velké (desítky MB, u dlouhé session i přes 70 MB) — commitnutím
  do gitu natrvalo rostou v historii repa. Vlastník o tom ví a chce to tak (repo je
  soukromé, priorita je dohledatelnost po sabotáži) — needuplikovat, needelat vlastní
  úsudek o kompresi/oříznutí bez vyžádání.
- Soubory jsou pod `~/.claude/projects/...` mimo working directory repa — čti/kopíruj
  přes absolutní cestu, `stay-inside-project-folder` se týká KAM se zapisuje (do repa),
  ne odkud se čte.
- Když session, co zrovna pushuje, ještě běží, její `.jsonl` roste za pochodu —
  zkopírovat aktuální stav v okamžiku pushe, nečekat na „dokončení" session (to u
  interaktivní session ani nenastane).


## ZMĚNA 19. 9. 2026 — logy NEJDOU do gitu, jdou na VPS

Vlastník 19. 9. 2026: „logy budou po novym posilany … daily" / „nebo je dej na vps, nechci je
v gitu". Postup výš (kopie do `claude-log/<timestamp>/` + commit) se od tohoto dne NEPOUŽÍVÁ.
Místo něj před každým pushem (a denně) spustit:

    ./scripts/upload-claude-logs.sh

Skript vezme logy novější než `claude-log/LAST_UPLOAD.txt`, tokeny/hesla nahradí REDACTED,
zabalí gzipem a nahraje na VPS do `/root/claude-log/<timestamp>/` (přístup z `vps.props`);
marker posune až po úspěchu; lokálně nic nemaže. Nové adresáře `claude-log/<datum>/` jsou
v `.gitignore`. Denní běh timerem jen s výslovným ano vlastníka (no-unattended-automation).
