---
name: design-consistency
description: Use in ANY project BEFORE writing or changing any UI - an app screen, a dialog, a component, a web page, a modal, a form. First look at the app (or web) and the components and design elements it ALREADY has - colors, tokens, dialogs, buttons, cards, spacing, typography - and reuse them verbatim. Never invent a new look, hardcode fresh colors, or ship a bare/default-styled element next to a styled one. Requested by the user 24.8. after an unstyled referral dialog on the web ("proc mas furt tendenci vsechno odflakat?").
---

# Design consistency — look first, then build with what exists

Every UI change starts with an inventory of what the project already has.
The user judges the result against the rest of the app/web, not in isolation;
a functional-but-plain element next to a styled one reads as sloppy work.

## Before writing any UI

1. **Find the design tokens** and use ONLY them:
   - app (Compose): `PsColors`/theme object, `Amber`, shared dimensions,
     `SectionHeading`, existing dialog composables (`*Dialog.kt` in
     `ui/components`), glyph components in `ui/icons`.
   - web: `style.css` custom properties (`--bg`, `--surface`, `--accent`,
     `--text`, `--muted`, `--line`), existing classes (`.chip`, `.cta`,
     `dialog#beta`, `.beta-actions`, `.ref-card`, …), `template.html`.
   - Hardcoded hex/px next to an existing token is a bug, not a shortcut.
2. **Find the nearest existing element of the same kind** (a dialog, a card,
   a form, a list row) and copy its structure and styling — same border,
   radius, padding, button style, headline color, backdrop. "X like Y" means
   parametrize Y, never a simplified rewrite ([[reuse-existing-ui-verbatim]]).
3. **Check both platforms/places** the element appears (app + web, mobile +
   desktop, photo + video) and keep them the same.
4. **Verify visually** when possible — screenshot (desktop/web) or bounds
   dump (mobile) — and compare against a neighbouring element of the project.

## Project facts (psippr)

- Look: black background, dark surface, amber/yellow accent (`#f5c518` on
  web, `Amber` in app), white/grey text, rounded corners (12–20 dp/px),
  amber 2 px border on dialogs, amber headline, ghost secondary buttons.
- Modal on the web = black window, amber 2 px border, 16 px radius, dark
  backdrop (`dialog#beta` look). Any new modal reuses that look (the user
  asked for div-based modals, 24.8.).
- No unrequested icons/emoji ([[no-unrequested-icons-emoji]]).

## Never

- Ship browser-default form controls, `alert()`/`prompt()`, or an unstyled
  block on a styled page.
- Introduce a second shade of the accent, a second card style, a second
  button style.
- Say "done" for UI you have not seen rendered next to its neighbours.
