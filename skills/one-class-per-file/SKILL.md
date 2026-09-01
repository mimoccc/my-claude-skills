---
name: one-class-per-file
description: HIGH PRIORITY rule for ANY Kotlin/KMP project - one class per file, every enum in its own file, every Compose component in its own file, files separated by function (data code in data packages, UI code in ui packages, etc.), and NO hardcoded values - enums where a closed set of variants fits, const object/class otherwise. Use whenever creating, moving, or reviewing Kotlin code, and during code cleanliness revisions.
---

# One class = one file, files sorted by function

HIGH PRIORITY rule, valid from the start of development in every project.
When touching code, leave it compliant — new code MUST comply immediately;
existing violations are fixed as part of code-cleanliness revisions (see below).

## The rule

1. **One class per file.** Every `class` lives in its own file named after it
   (`FooBar` → `FooBar.kt`). No unrelated top-level classes sharing a file.
2. **Every enum in its own file.** `enum class Tab` → `Tab.kt`. Never nested
   inside an unrelated file just because it is "small".
3. **Every Compose component in its own file.** Each public/reusable
   `@Composable` (a screen, a tile, a dialog, a bar…) gets its own file named
   after it (`UserTile` → `UserTile.kt`). Tiny private helpers used ONLY by that
   component may stay in the same file below it.
4. **Files separated by function (package = role):**
   - data/persistence/store/serialization → `data` packages
   - UI composables/screens/components/theme → `ui` packages (`ui/components`,
     `ui/screens`, `ui/theme`…)
   - view models / app state → `vm`
   - domain/core models and pure logic → `core` (or `domain`)
   - platform/p2p/network layers → their own packages (`p2p`, `disco`, `call`…)
   A file must not mix roles (no UI composable inside a data store file, no
   persistence inside a screen file).
5. **No exceptions for "closely bound" declarations** (tightened 1. 9. 2026:
   "jedna class/object/enum jeden soubor i kdyby jich melo byt milion").
   - A sealed hierarchy is ALSO split: Kotlin only requires subclasses in the
     same package+module, not the same file. The sealed parent keeps its file;
     every implementation gets its own.
   - If the hierarchy is SERIALIZED (kotlinx polymorphic/sealed), the class FQN
     is the wire discriminator — pin the ORIGINAL name with `@SerialName(...)`
     on every subclass BEFORE moving, and add a wire-compat test, or old
     clients stop understanding the new build.
   - A `private` top-level class moved to its own file becomes `internal`
     (file-private visibility cannot cross files).
   - Only nested types that are genuinely part of their parent's contract
     (a companion object, an inner class using outer state) stay nested.
6. **No hardcoded values.** Magic numbers, magic strings, repeated literals and
   inline variant strings ("red"/"green", "chat"/"dates"…) are forbidden in
   logic and UI code:
   - a **closed set of variants** → an `enum class` (own file, rule 2); switch
     on the enum, never on raw strings/ints;
   - a **standalone constant** (timeout, limit, key, URL, dimension…) → a named
     `const val` in a dedicated constants `object`/class (or the owning class's
     companion), named by meaning (`BYE_GRACE_MS`), never a bare literal at the
     call site;
   - the same literal must never be duplicated across files — one definition,
     referenced everywhere.
7. **App-wide events via a typed Flow event bus — where it fits.** For
   cross-cutting events between app parts, prefer the mimoccc/tvapp style
   (see `PauseEvent` + tvlib `EventBusCore`/`PostEvent`): each event is a
   `data class` in its own file under an `events` package, fired with
   `postEvent(SomeEvent(...))` and consumed with `observeEvent<SomeEvent> {}`
   over a shared Flow. Use it when unrelated modules/screens must react to the
   same signal (pause, refresh, logout…) instead of ad-hoc singleton
   `MutableStateFlow` counters or callback plumbing. Not mandatory everywhere —
   plain state flows owned by a single state holder stay as they are; the bus
   is for genuine broadcast events, only where needed.

## Why

- Monolith files (a 4000+ line Screens.kt) make review, navigation, merges and
  targeted fixes slow and error-prone; the user explicitly demands this
  structure as a standing, high-priority requirement.

## How to apply

- **New code:** never add a second unrelated class/enum/composable to an
  existing file; create the properly named file in the properly named package.
- **Moving code:** plain moves, no behavior changes mixed in (see
  kotlin-kmp-refactor-safety); keep git history readable — move in dedicated
  commits ("split X into files"), separate from logic changes.
- **Review/cleanliness passes:** flag every violation found; large legacy
  monoliths are split incrementally (screen by screen, component by component)
  in agreed batches, each batch compiled + installed before the next.
- **Verification:** after a split batch, the project must compile for all
  targets touched (desktop + android at minimum) before commit.

## Mechanical-split lessons (paid for on 1. 9. 2026)

- **Operator imports are textually invisible.** `import androidx.compose.runtime.getValue`/
  `setValue` (delegation `by`), `provideDelegate`, `component1/2` never appear
  as tokens in the body — an "unused import" cleanup that greps for the name
  WILL remove them and break every `var x by remember`. Whitelist them.
- **Raw strings and char literals break naive brace counting.** `"""…"""` and
  `'{'`/`'"'` desync a line-based parser; any automated splitter must lex
  strings, raw strings, char literals and comments before counting brackets.
  Verify by compiling EVERY touched module before commit, and check files that
  contain `"""` by hand.
- **Never split generated code** (`build/`, `generated/`, uniffi bindings) —
  the generator recreates the old layout on next run.
