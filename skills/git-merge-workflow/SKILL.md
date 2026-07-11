---
name: git-merge-workflow
description: Use when finishing a task in this repo (psippr) and getting the change into main — this project does not use pull requests; work goes to main via rebase + fast-forward push.
license: Apache-2.0
metadata:
  author: mimoccc
  version: "1.0.0"
---

# Git merge workflow (no pull requests)

This project's owner does not want GitHub pull requests. Work lands on
`main` via a linear rebase + fast-forward push instead.

## Per-task commits

- One commit per task. Do not bundle unrelated tasks into one commit, and
  do not split a single task across multiple commits.
- Commit message is a single line: short, imperative, no colon, no body/
  description paragraph. Example: `Přidat debug APK do release buildu`
  (not `Add debug APK: include it in release build\n\nLonger explanation...`).

## Landing on main — no PRs

1. Develop on a feature branch (`claude/...`) as usual.
2. Before merging, fetch and compare with `origin/main`:
   ```
   git fetch origin main
   git merge-base --is-ancestor origin/main HEAD && echo "fast-forward possible"
   ```
3. If the feature branch is a strict fast-forward of `origin/main` (all of
   main's commits are already in the branch's history, branch is just ahead),
   push it straight onto main — no PR, no merge commit:
   ```
   git push origin <feature-branch>:main
   ```
4. If it is **not** a fast-forward (main has moved with unrelated commits),
   rebase the feature branch onto `origin/main` first, keeping each task's
   commit separate (no squashing unless explicitly asked):
   ```
   git rebase origin/main <feature-branch>
   ```
   then repeat step 3. Resolve conflicts during the rebase rather than
   merging or force-pushing over main.
5. Never `git push --force` to `main`. If a fast-forward isn't possible
   after rebasing, stop and ask before doing anything more invasive.

## Do not

- Do not run `gh pr create` / open a pull request for this repo unless the
  user explicitly asks for one in that specific instance.
- Do not squash multiple tasks' commits together on main.
- Do not merge with a merge commit (`git merge --no-ff`) — history on
  `main` stays linear.
