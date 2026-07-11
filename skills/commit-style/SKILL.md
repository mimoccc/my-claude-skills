---
name: commit-style
description: Use before every git commit in this repo (psippr). Enforces the project's commit conventions - short English title without colon, no Co-Authored-By, stepwise commits, never break the existing commit/CI flow.
---

# Commit style for psippr

Every commit in this repo follows these rules — no exceptions:

1. **English only.** Commit titles are always written in English, even though the
   conversation and code comments may be Czech/Slovak.
2. **Short title, no colon.** One lowercase-ish imperative line, e.g.
   `fix album viewer crash inside scroll column`. No `feat:`/`fix:` prefixes, no colon.
3. **No Co-Authored-By** and no other trailers — plain title (body only if truly needed).
4. **Commit per step.** Each logically separate change gets its own commit as work
   progresses; don't batch a day of work into one commit.
5. **Don't break the commit/CI flow.** Push to main goes rebase + fast-forward
   (`git pull --rebase origin main` first). Every push to main triggers the bumpVersion
   workflow (version bump + tag + Release build) — never delete/force-move tags, never
   force-push over the bot's `version bump to X.Y.Z` commits.
6. Before pushing, builds must pass locally: `:androidApp:assembleDebug` at minimum,
   `:androidApp:assembleRelease` (R8) plus `:shared:compileKotlinDesktop` and
   `:shared:compileKotlinWasmJs` when shared/build files changed.
