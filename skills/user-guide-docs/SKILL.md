---
name: user-guide-docs
description: Use in ANY KMP project when a user-facing feature is added, changed, or removed, when screenshots of the app exist or can be taken, or when the user asks for a user guide/manual. Every KMP project must have an end-user guide in doc/ (guide.md EN + guide-cs.md CZ + doc/img screenshots) — create it if missing, update it when features change.
---

# User guide documentation (doc/guide.md)

Every KMP app project keeps an **end-user manual** (not developer docs) in
the repo, editable by both the user and Claude:

```
doc/
  guide.md       # English version
  guide-cs.md    # Czech version (mirror of guide.md)
  img/           # screenshots, NN-topic.png, english names
```

This is different from root `<topic>.md` guides (see root-markdown-guides
skill): those document *setup steps for the developer*; `doc/guide.md`
documents *how to use the app*, for an ordinary person.

## When to act

- A user-facing feature is added/changed/removed → update BOTH language
  versions in the same commit as the feature (or right after).
- The project has no `doc/guide.md` yet → create the full structure.
- The user asks for a guide/manual/navod for the app → this skill, not
  root-markdown-guides.

## Writing rules

1. **Written for everyone** — no jargon (no "nodeId", "P2P engine", "TTL");
   explain in plain words what the person sees and what happens. Short
   sentences, concrete UI names as they appear on screen.
2. **Both languages always** — guide.md (EN) and guide-cs.md (CZ) must stay
   in sync; cross-link them at the top (`> Česká verze: …` / `> English
   version: …`). More languages only if the user asks.
3. **Chapters follow the app's screens** (first start, each main tab, own
   profile/settings, privacy, payments). Promo/VIP or license chapters go
   LAST. Use `<img src="img/NN-name.png" width="300">` next to the chapter
   it illustrates; tables for settings/price lists.
4. **Truth from the code** — feature list comes from the strings resources
   (e.g. `shared/src/commonMain/composeResources/values/strings.xml`) and
   the actual UI, never from memory. Sweep the string keys to catch features
   you'd forget (spam lists, limits, hidden switches).
5. **Nothing private in screenshots** — capture on a connected device
   (uiautomator dump before every tap — no blind taps; overlapping bounds:
   prefer the innermost clickable node; after a keyboard opens, RE-dump —
   the whole layout shifts). Review every image before committing: no real
   conversations, wallets, tokens, or third-party private data. Protect
   what must stay (faces of third parties, private texts, explicit album
   covers) by pixelating regions in place:
   `magick img \( +clone -crop WxH+X+Y +repage -scale 4% -scale 2500%
   -resize WxHtml! \) -geometry +X+Y -composite img` — and if unprotected
   versions were already committed, AMEND the commit so they never reach
   history. Beware FLAG_SECURE states (e.g. non-VIP renders black
   screencaps) — capture such screens on desktop or describe them in text.
   For chat/social screenshots, **stage a demo conversation between the
   user's own devices** (phone ↔ desktop; ask the user to tap a reply on
   the other device — desktop input injection is unavailable on Wayland)
   instead of showing real conversations. For "now playing" features, drive
   a real player (e.g. open a URL in NewPipe via
   `am start -a android.intent.action.VIEW -d <url> org.schabi.newpipe`
   and tap its background-play action).
6. **Update discipline** — a stale guide is worse than none. When behavior
   an existing chapter describes changes, fix the chapter in the same
   commit. Keep image filenames stable so diffs stay small.

## Creating from scratch (missing in a KMP project)

1. Inventory features: strings resources + main navigation tabs + settings
   screens.
2. Capture screenshots of each main screen (phone via adb screencap, or
   desktop via xwininfo + import on XWayland).
3. Write guide.md (EN), then mirror to guide-cs.md (CZ).
4. Commit `doc/` in one commit; screenshots live in git (private repos) —
   keep them reasonably small (full-res phone PNGs are fine, ~5 MB total).

## App tour video

A screen-recorded tour can live at `doc/promo-tour.mp4` — separate from the
guide, never linked as a guide chapter. **A raw click-through communicates
nothing** (learned the hard way): the video must TELL what the app does —
every segment gets a text caption naming the feature being shown (ffmpeg
drawtext overlay or inter-title cards), pacing slow enough to follow, and
the feature list must be complete before recording (prepare demo content
with the user first — empty albums or feeds show nothing). To (re)create:

1. Record one segment per chapter on the phone:
   `adb shell screenrecord --time-limit N --bit-rate 8000000 /sdcard/segX.mp4`
   — FOREGROUND (blocking) whenever the segment needs no taps (idle screens):
   backgrounded adb processes get orphaned and killed, leaving files without
   a moov atom (unreadable). Background only segments that need parallel
   taps, keep them inside one shell command that sleeps past the time limit,
   and leave several seconds gap before the next recording. VERIFY the
   screen (uiautomator dump) before each segment — navigation drifts
   silently. Static screens encode shorter than wall time — that's normal.
2. Normalize: `ffmpeg -i seg.mp4 -vf "scale=540:-2,fps=30,format=yuv420p"
   -c:v libx264 -crf 23 -an n_seg.mp4`; make a title card from
   `color=c=black` + drawtext.
3. Concat with the concat demuxer (`-f concat -c copy`) in guide-chapter
   order; keep the result around 1 MB.

## PDF manuals (createDocumentation)

Each md in doc/ becomes a standalone PDF — language versions are separate
documents with NO cross-links between them. Make `doc` a Gradle module with
a `createDocumentation` task (see psippr: `doc/doc.gradle.kts` +
`buildSrc/CreateDocumentationTask.kt`) rendering md → XHTML (commonmark +
gfm-tables) → PDF (openhtmltopdf, pure JVM — no pandoc/chrome, CI-safe).
Manual look, not IT-doc look: PSippr-style brand header on every page
(running element + accent rule), footer with `page / pages` counter, brand
accent on headings/tables, embedded DejaVu for diacritics, images ~240px
centered. Give the task an IDE run action, gitignore the generated PDFs,
and wire them into the release pipeline (collect step + CI workflow job
that runs on a host with fonts) so they ship with each release (incl.
WhatsApp post). Kotlin gotcha: `doc/*.md` inside a KDoc opens a NESTED
comment — reword, don't glob, in comments.

## Follow-ups worth offering

- In-app onboarding for fresh installs reusing the same chapters.
