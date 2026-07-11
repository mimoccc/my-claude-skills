---
name: sync-skills
description: Use whenever a skill in .claude/skills is added or modified. Mirrors skills to github.com/mimoccc/my-claude-skills - one commit per skill, intelligent two-way merge (ask user on conflict), push WITHOUT asking (standing exception to ask-before-push).
---

# Sync skills to mimoccc/my-claude-skills

Whenever a skill is added or changed in `.claude/skills/`, sync it to the
shared skills repo. The push of this sync is pre-authorized — do NOT ask
(standing exception to the `ask-before-push` skill).

## Working copy

- Local clone lives at `~/.cache/my-claude-skills` (SSH remote
  `git@github.com:mimoccc/my-claude-skills.git`, branch `main`).
- If missing, clone it; otherwise `git pull --rebase` first so the merge sees
  the current remote state. Never force-push.
- Repo layout mirrors the source: `skills/<skill-name>/…` at the repo root.
- Sync ONLY `.claude/skills/` content. Never sync `settings.json`,
  `settings.local.json`, or other `.claude` files (local machine config,
  may contain permissions/secrets).

## Intelligent merge (two-way)

For every skill name present locally or in the repo:

1. **Only local** → copy into repo, commit `add skill <name>`.
2. **Only in repo** → copy into the project's `.claude/skills/` (bring it in),
   and commit it to the project repo per its commit rules.
3. **Both identical** → nothing to do.
4. **Both differ** → merge intelligently:
   - If the differences are complementary (different files, or clearly
     additive sections that don't contradict each other), merge both sides
     into one version, write it to BOTH places, commit `update skill <name>`.
   - If the same content genuinely conflicts (same section says different
     things), STOP and ask the user which version wins (AskUserQuestion with
     both variants). Never silently overwrite either side.

## Commits and push

- **One commit per skill** — `add skill <name>` / `update skill <name>` /
  `remove skill <name>`. Short English title, no colon, no Co-Authored-By,
  no trailers.
- After all skill commits: `git push origin main` — without asking.
- If the project's `.claude/skills` is tracked by the project repo (psippr:
  it is), also commit the skill changes there per that repo's commit style;
  pushing the PROJECT repo still requires asking per `ask-before-push`.
