---
name: no-unattended-automation
description: Use in ANY project BEFORE creating, enabling, or modifying anything that runs by itself without the user pressing a button - CI schedule/cron triggers, systemd timers, OS cron jobs, webhooks that fire workflows, auto-retry loops, watchdogs, periodic backups. Such automation NEVER ships without the user's explicit yes given AFTER hearing frequency and price per month. Also use when auditing a repo for automation the user may not know about.
---

# Nothing runs on its own without the owner's informed yes

## Why this skill exists

On 2026-08-13 three scheduled workflows (a VPS watchdog, a peers-table mirror,
a daily ledger backup) were added to a private repo as a side product of server
work - useful, but never ordered and never announced. The owner discovered them
the next day **in the GitHub billing page**, paying for runs while "doing
nothing". Their verdict: automation created without their knowledge is fraud,
however useful it is. Full entry: `ai-incidents.md` 2026-08-14.

## What counts as unattended automation

Anything that will execute later without a human starting it:

- `schedule:`/cron triggers in CI workflows (GitHub Actions, Codemagic, ...)
- systemd timers, OS crontabs, `at` jobs - on any machine, including a VPS
- repeated polling loops left running (watchers, monitors, keep-alives)
- webhooks or repository events wired to start builds/deploys
- auto-restart / auto-retry / auto-update mechanisms on servers or devices
- anything with "daily", "hourly", "watchdog", "mirror", "sync" in its purpose

A one-shot command the user asked for is fine. The moment it gains a *repeat*,
it falls under this skill.

## The rule

1. **Announce BEFORE creating.** Name the thing, what it does, **how often it
   runs**, and **what it costs per month** (CI minutes on private repos are
   paid; macOS is 10x, windows 2x; artifact storage counts too). One short ask,
   then WAIT for an explicit yes. Silence, or the user not objecting, is NO -
   same as ask-before-own-ideas.
2. **"Useful" is not consent.** The incident crons were genuinely useful (one
   saved the promo-code ledger the very next morning). Useful and unauthorized
   is still unauthorized.
3. **Piggybacking is the trap.** This never happens as "add a cron" tasks; it
   happens as a side product of a bigger job ("while packaging the server,
   I'll add a watchdog"). The bigger job's approval does NOT cover the
   automation - it needs its own yes.
4. **Keep an inventory the user can see.** Every approved automation gets a
   line in a root markdown file (`automation.md` or the relevant guide): what,
   where, schedule, monthly cost, how to disable it. When infra changes
   (server move, repo split), re-list the inventory to the user.
5. **Modifying counts too.** Raising a frequency, re-enabling a disabled
   workflow, widening a trigger - each needs the same informed yes.
6. **When in doubt, audit.** Asked anything about costs, billing, or "what runs
   here"? Grep for `schedule:` in CI configs, `systemctl list-timers` and
   `crontab -l` on servers, and report the full list with prices - including
   things the user may have forgotten.

## The ask, concretely

> Chci přidat X, které poběží samo (frekvence Y), na privátním repu to bude
> stát ~$Z měsíčně. Bez něj se stane W. Přidat?

Options via `AskUserQuestion` when there is a real choice (frequency tiers,
enable now vs later). No burying the ask inside a progress report.

## If it already happened

Discovering an unannounced automation (yours from an earlier session or
anyone's): stop it or surface it immediately, log it via ai-incident-report,
and never silently "fix it forward".
