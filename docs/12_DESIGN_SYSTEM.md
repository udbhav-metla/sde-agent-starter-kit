---
doc_id: "12"
title: "Design System"
status: "baseline"
owner: "Frontend Lead"
version: "1.0"
last_updated: "2026-10-12"
depends_on: ["07_UI_UX_SPEC.md"]
---

# Design System

The detailed screen behavior and UX copy live in `07_UI_UX_SPEC.md`. This file captures reusable implementation tokens.

## Principles
- Quiet, light-first, Apple-inspired restraint; not a pixel-for-pixel Apple clone.
- Neutral surfaces and typographic hierarchy do most of the work.
- Alexa-inspired light blue is a secondary accent, never a neon text theme.
- Color supplements labels; it never carries status alone.
- Use actual product language and report observable outcomes.

## Tokens
```css
:root {
  --color-canvas: #F5F5F7;
  --color-surface: #FFFFFF;
  --color-surface-muted: #F0F2F5;
  --color-ink: #17191D;
  --color-ink-secondary: #626873;
  --color-ink-tertiary: #858B95;
  --color-line: #E2E5E9;
  --color-alexa-blue: #58C7F3;
  --color-alexa-blue-strong: #168AC0;
  --color-alexa-blue-wash: #EAF8FE;
  --color-success: #21845B;
  --color-warning: #A96812;
  --color-danger: #C53B43;
  --radius-panel: 12px;
  --radius-control: 10px;
  --space-unit: 8px;
  --font-ui: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  --font-code: "SFMono-Regular", ui-monospace, "Cascadia Code", monospace;
}
```

## Rules
- `#58C7F3` is too light for small text on white; use `#168AC0` for text/controls requiring contrast.
- Use an 8 px spacing base and 10–14 px panel radius.
- Prefer thin borders over shadows.
- Avoid decorative gradients, glassmorphism, giant metric cards, and looping glow.
- Use sentence case and verbs in button labels.
- Test color contrast against WCAG 2.2 AA.
