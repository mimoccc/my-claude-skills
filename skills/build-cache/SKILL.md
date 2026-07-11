---
name: build-cache
description: Use when builds in this repo (psippr) feel slow, when adding new modules/tasks, or when touching gradle.properties, settings.gradle.kts, CI workflows, or the Rust build scripts. Documents every cache layer in the project, how to verify it works, and rules that keep builds fast.
---

# Build cache & speed for psippr

Baseline (2026-07-11, 8-core/15G machine): no-op `assembleDebug` ~5 s (config cache
hit), incremental after one shared file change ~15 s (`:shared:compileAndroidMain`
dominates), cold Kotlin daemon adds ~50 s to the first build. R8 release build is
minutes, not seconds — always the last thing to verify, not the dev loop.

## Cache layers (all must stay on)

1. **Configuration cache** — `org.gradle.configuration-cache=true` (+ `.parallel=true`).
   No-op builds run ~1–5 s only because of this. Never add configuration-time logic
   that reads changing files/env without declaring them; it invalidates every build.
2. **Build cache** — `org.gradle.caching=true`. Reverting a change re-uses cached
   task outputs (verified: same-content rebuild drops 68 s → 1 s). Retention is
   extended to 30 days via `~/.gradle/init.d/cache-retention.gradle.kts`
   (machine-level, Gradle 9 does not allow this in settings.gradle.kts).
3. **Kotlin incremental compilation** — `kotlin.incremental=true`,
   `kotlin.incremental.wasm=true` (wasm is experimental; if webApp builds start
   failing weirdly, this flag is the first suspect).
4. **VFS watching** — `org.gradle.vfs.watch=true`, fast up-to-date checks.
5. **Daemons + GC** — gradle daemon 4G / kotlin daemon 3G (`kotlin.daemon.jvmargs`),
   both with `-XX:+UseParallelGC` (R8/dex are throughput-bound; 2G used to choke R8
   in GC for 17+ min). Changing any jvmargs restarts daemons = one slow build.
6. **Rust natives** — `scripts/build-*-android.sh` skip when the `.so` is newer than
   the crate sources (gossip) or exists at all (iroh). Cargo's own `target/` dir is
   the cache. They are `Exec` tasks without declared outputs — they run every build
   but exit in ~ms via those guards. Keep the guards when editing the scripts.
7. **CI** — `gradle/actions/setup-gradle@v4` (gradle home cache),
   `actions/cache` for `~/.konan` and the AppImage tool. CI has no Rust toolchain;
   native builds skip silently (bindings are committed).

## Verifying caches after build changes

- No-op check: `./gradlew :androidApp:assembleDebug -q` twice — second run must be
  seconds and say nothing. If tasks re-execute, something broke up-to-date checks.
- Config cache check: output must say `Reusing configuration cache.`; if it keeps
  saying `Calculating task graph`, find what invalidates it
  (`--configuration-cache-problems=warn` prints the reason).
- Cache-hit check: make a change, build, revert it, build — the revert build should
  be ~1 s (FROM-CACHE), not a recompile.
- Profile when unsure: `./gradlew <task> --profile`, report lands in
  `build/reports/profile/`. Beware: profiling an unchanged source tree measures
  cache hits, not real compile cost — make a *unique* change first.

## Rules

- Don't add `Exec`/`doLast` tasks without inputs/outputs into the compile path —
  either declare them or add a cheap early-exit guard like the Rust scripts.
- Don't disable configuration cache "temporarily" to work around a plugin — fix the
  plugin usage; a disabled config cache costs every future build ~10 s.
- Big `:shared` is the incremental bottleneck; when it grows further, split features
  into modules (`:db`, `:gossip`, `:phone` pattern) instead of growing `shared`.
- The dev loop is `assembleDebug`; run `assembleRelease` (R8) only as the final
  pre-push verification (see commit-style skill).
