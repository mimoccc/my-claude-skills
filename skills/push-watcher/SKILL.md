---
name: push-watcher
description: Use the moment the user says they pushed ("pushnul jsem", "pushol som", "pushed", "push je tam") in ANY project with GitHub Actions. Start a background watcher on the runs the push triggered; on failure pull the real error, write the diagnosis into the per-platform CI journal (ci-journal/<platform>.md) and, when our own change caused it, into ai-incidents.md.
---

# Push watcher

Po slovech „pushnul jsem / pushol som / pushed" NEČEKAT na dotaz — rovnou:

1. `git fetch` + `git pull --ff-only` (lokální repo dorovnat, jinak příští
   install skončí na VERSION_DOWNGRADE).
2. `gh run list --limit 5` — najít běhy spuštěné tím pushem (v psippr:
   bumpVersion → Release pro nový tag).
3. Spustit hlídač NA POZADÍ (run_in_background smyčka s `gh run view --json
   status,conclusion`, interval ~60 s) a pokračovat v práci.
4. Po doběhnutí:
   - **success** → jedna věta uživateli (verze, u psippr zkontrolovat, že
     v releasu je reálná `.ipa` — krok umí hlásit success i po ARCHIVE FAILED).
   - **failure** → `gh run view --log-failed`, vytáhnout PRVNÍ skutečnou
     chybu (`e: file...`, `##[error]`, ARCHIVE FAILED), určit platformu
     z názvu jobu a:
     a) do `ci-journal/<platforma>.md` doplnit k záznamu od CI řádek
        „proč + poučení" se skutečnou příčinou (záznam s fakty tam už
        zapsal job notify-failure; když chybí, založit celý),
     b) když příčinou byla naše změna → záznam i do `ai-incidents.md`
        (formát: co, commit, škoda, oprava, pravidlo),
     c) opravit příčinu, commitnout; push jen na pokyn.
5. Nikdy nehlásit „build OK" z tvrzení kroku — ověřit artefakt/asset.

Deník je k ničemu, když se jen zapisuje: před dalším pushem si projít poslední
záznamy platformy, která padá (u psippr `ci-journal/ios.md`).
