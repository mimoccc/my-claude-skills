---
name: ask-before-push
description: Use whenever a git push comes into consideration. NEVER push a project repo on your own initiative - ask the user before EVERY such push. Single standing exception - the skills mirror push to mimoccc/my-claude-skills, which goes without asking after every skill change.
---

# Never push the project - ask every time

1. **Default: no push, ever.** Finishing work does NOT imply pushing it.
   Commit locally per step and leave the push to the user.
2. **Ask before EVERY push of a project repo.** This includes:
   - pushes the user asked for earlier in the session,
   - repair pushes for a build you broke,
   - "the run is already cancelled, let's start a good one",
   - any branch or tag of the project the work came from.
   Even in automode. Even when the user's stated goal (an artifact, an
   install, a CI verification) cannot happen without the push - say that and
   let them decide.
   **Standing exception:** the skills mirror push to
   `mimoccc/my-claude-skills` (see `sync-skills`) goes WITHOUT asking, always,
   after every skill change. It touches no project repo, triggers no release
   and costs nothing. Never push the source project in the same breath -
   that one always needs its own ask.
   **Always name the repo (rule added 2026-08-05).** Never write "pushed" on
   its own - the user reads that as "pushed psippr/main" and panics about a
   release going out. Say which repository and branch went out
   ("pushnuto do mimoccc/my-claude-skills (mirror skillů), psippr NE") and, in
   the same breath, that the project repo stayed local with N commits ahead.
   The two repos are reported separately, never merged into one sentence.
3. **A "push" from the user covers exactly the commits that existed when they
   said it.** It never carries over.
   **Hard gate before typing `git push`:** re-read the last few user messages.
   There must be a present-tense imperative aimed at exactly the commits you
   are about to send. If you have made *any* commit since that message, or the
   set of commits differs in any way from what was described, the consent has
   expired - ask again.
   - An option picked in an AskUserQuestion dialog covers only the work
     described in that option's text. Extra commits made afterwards are NOT
     covered.
   - Approval of a *fix* ("good that you're fixing it") is not approval of a
     *push*.
   (Escalated 2026-07-25, 2026-07-28 and twice on 2026-07-29 - every push to
   main costs a CI release cycle, macOS minutes included, so an unwanted push
   burns real money.)
4. **Cancelling a running CI run is the user's call too** - offer the choice,
   don't decide and then report it.
5. **Commits are not gated.** Committing locally per step stays autonomous;
   only the push is restricted.
6. **One ask per push moment.** If several commits are ready, one confirmation
   covers pushing them together; don't ask per commit. State exactly which
   commits go out.
