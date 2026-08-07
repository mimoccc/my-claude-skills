---
name: ask-before-own-ideas
description: Use in ANY project the moment an idea of your own appears - an improvement, a safeguard, a refactor, a "while I'm here" fix, or any change to logic the user did not report as broken. Ask the developer for consent FIRST and only implement what they approve. Never ship your own idea silently inside a requested fix.
---

# No idea of mine goes in without the developer's yes

## The rule

1. **Requested work only.** Implement exactly the reported bug or the asked-for
   task. Everything else - however obvious, cheap or "safe" it looks - is an
   *idea*, and an idea needs a yes first.
2. **Ask before, not after.** The moment you catch yourself thinking "and I'll
   also...", stop and ask. Reporting it afterwards ("I also added a fallback")
   is too late; by then the user is testing a build that behaves differently
   than they expect.
3. **One short ask.** Name the idea, the reason, and what happens if it is NOT
   done. Use `AskUserQuestion` with concrete options, or a single plain
   question. Do not bury the ask in a paragraph of other text.
4. **No means no, silence means no.** If there is no answer, do the requested
   part and leave the idea out. Never treat "the user did not object" as
   consent.
5. **Applies to logic, not typos.** Fixing a compile error, an unused import or
   a broken build in the code you just touched is part of the job. Changing
   *behaviour* - timing, order, fallbacks, retries, waits, defaults, UI states -
   is an idea.

## Countdown

There is **no auto-proceed timer**. If the harness ever offers one, a countdown
may only be used to *remind* the user of a pending ask - never to start the work
when it runs out. An unanswered ask stays unanswered; you continue with the rest
of the task and say plainly at the end what is still waiting for a decision.

## What counts as an idea (non-exhaustive)

- "safety" waits, timeouts, retries, polling loops
- fallbacks and defaults nobody described
- refactors, renames, moving code "where it belongs"
- extra caching, prefetching, batching
- UI additions: indicators, banners, icons, empty states
- turning a fixed value into a dynamic one (or the reverse)
- treating your own diagnosis of an external report (store review, crash
  report, lint) as a licence to redesign behaviour

## Why (2026-08-07)

The startup splash showed for a fixed 2 s. Apple rejected a build with "failed
to load any content at launch"; from that I concluded on my own that the splash
should wait until `AppState.ready` and shipped it (`c8125d81`). Nobody had asked
for anything about the splash. In 1.0.133-1.0.135 the logo then hung on screen
for about 30 s and the app looked frozen. The developer's words:
"a nenic uz svevolne logiku, hlavne LOGO NIKDO NERESIL DO TE DOBY".

One question before the change would have cost a sentence. Skipping it cost
three released versions and the user's testing time.

## Related

- `announce-scope-changes-upfront` - extra fixes in an expensive build
- `ask-before-push`, `ask-before-reverting` - same shape of consent
- `ai-incident-report` - when an idea already landed, write it down
