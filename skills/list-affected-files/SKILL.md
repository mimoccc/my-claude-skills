---
name: list-affected-files
description: Use at the END of EVERY prompt in ANY project where files were created, edited, or deleted. Print the list of affected files as clickable links (file_path:line) so the user can open each one for review. Applies to every single prompt, including small fixes and mid-turn tasks.
---

# List affected files after every change

After ANY prompt where files were touched (Write/Edit/delete/generated), the
final answer MUST end with a list of the affected files as clickable links.

1. **Every prompt, no exceptions.** One edited file or twenty — the list is
   always printed. Skipped only when the prompt touched no files at all.
2. **Format: one file per line, clickable.** Use the `file_path:line` form
   (relative to the repo root) so the IDE/terminal opens it on click; point
   `line` at the most relevant change (1 when whole-file):

   ```
   Změněné soubory:
   - shared/src/commonMain/kotlin/org/mjdev/psippr/provider/ContentProvider.kt:42
   - db/src/commonMain/sqldelight/org/mjdev/psippr/db/psippr.sq:150
   ```
3. **Complete, not curated.** Deleted and newly created files belong on the
   list too (mark deletions with `(smazán)`). Files touched by scripts or
   generators you invoked count as affected; purely derived build output
   (`build/`) does not.
4. **Purpose: review.** The user opens each link to check the change — the
   list is the review queue, so its order should follow importance, not
   edit order.
