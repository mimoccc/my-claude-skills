---
name: backup-data-before-risky-change
description: Use in ANY project BEFORE an operation that could damage or lose the app's live data on a device or machine - storage schema/format changes, migrations, wipe/reset paths, uninstall or reinstall with a different signature, media layout changes, or any destructive shell command. Back the data up FIRST, say where the backup is, and only then run the operation.
---

# Back the data up before you can break it

The user's device holds real, irreplaceable data — messages, photos, albums,
identity keys. A change that touches how data is stored can corrupt it, and there
is no undo. **Back it up first. Every time. Even when you are sure.**

## When this applies

Anything that could rewrite, relocate, delete or reinterpret stored data:

- storage schema or serialization format changes (`.sq` tables/columns, changed
  field names or types in persisted models, changed media file layout/naming),
- migrations, or code that rewrites existing records in place,
- `wipeAll` / reset / "delete profile" / "clear data" paths, including testing them,
- uninstall, reinstall with a different signing key, or install of a build with a
  different `applicationId` that shares external storage,
- device takeover / clone / sync work that writes into the receiving side,
- destructive shell commands (`rm -rf`, `adb shell pm clear`, dropping a table,
  overwriting a file with `>`).

Reading data is fine. Writing, moving or deleting it is not — back up first.

## How to back up

Prefer the app's OWN export if it has one — it is the format the app can restore.
In psippr that is `exportAppData()` / `importAppData()` (`core/Backup.kt`,
`BACKUP_FILE_NAME = "psippr.zip"`), reachable in the UI as Settings → Me →
Backup (export/import). Ask the user to run the export and keep the file.

When the app has no export, or the operation runs from the outside:

- **debuggable build:** `adb exec-out run-as <pkg> tar -c -C /data/data/<pkg> .`
  redirected to a file on the computer,
- **non-debuggable build:** you cannot read app data — say so plainly and ask
  the user to export from inside the app before you continue,
- **desktop/server:** copy the data directory (or `pg_dump`/DB dump) to a
  timestamped file outside the working tree first.

Never put the backup where the risky operation will run.

## Rules

1. Back up BEFORE the change, not after it goes wrong.
2. Tell the user **where** the backup is and **how** to restore it — a backup
   nobody can find is not a backup.
3. If you cannot back up (no access, non-debuggable build), do not proceed on
   your own: say why, and let the user decide.
4. Verify the backup exists and is non-empty before running the operation.
5. Never delete a backup to tidy up.
