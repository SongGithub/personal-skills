---
name: document-design
description: A reusable HTML document design system for CVs, one-pagers and short reports — design tokens, layout, typography, print-to-PDF rules and accessibility. Use when generating or restyling a self-contained HTML document meant to be read on screen or printed to PDF.
---

# Document design

One design system for self-contained HTML documents. The aim: correct on screen, clean when printed to PDF, and no build step — a single file you can open anywhere.

Copy `references/cv-template.html` as a starting point; it already wires up everything below.

## Design tokens

Put every colour and surface in custom properties at `:root`, with a dark-theme override. Never hard-code a hex value in a rule; that is what makes the document themeable and printable.

```css
:root {
  --doc-background: #ffffff;
  --doc-background-mid: #eef0ee;   /* page surround */
  --doc-border-light: #e3e3e0;
  --doc-text-primary: #1d1f22;
  --doc-text-secondary: #5f6368;
  --doc-accent: #1f6f5c;           /* one accent, used sparingly */
  --doc-accent-soft: #e7f1ee;      /* chip/tint background */
}
html[data-theme='dark'] {
  --doc-accent: #4fbfa3;
  --doc-accent-soft: #16332b;
}
```

Rules:

- **One accent colour.** It marks section headings, the role/company name, bullet markers and nothing else. Accent everywhere reads as decoration.
- **Two text colours.** Primary for content, secondary for metadata (dates, locations, notes).
- **Tint, don't fill.** Use `--doc-accent-soft` for chips rather than solid accent blocks.

## Layout

- **Page width 820px maximum**, centred, with a 24px top margin. Wider than this and the line length hurts readability.
- **Page padding 38–42px.** Padding carries the visual weight, so no outer border is needed.
- **Page surround** is `--doc-background-mid` so the white page reads as a sheet.
- Sections stack with a **15px gap**. Structure comes from spacing and a single hairline under each section heading, not from boxes or panels.

## Typography

- **System font stack**, no webfonts: `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`. Nothing to load, nothing to fail offline.
- **Base is small**: 12.8px on screen with 1.38 line-height. This is a document, not a blog post — density is a feature.
- **Scale**: name 28px/700, section heading 11.5px/700 uppercase with 1.3px letter-spacing, role title 13.5px/700, body 12–12.5px, metadata 11px.
- **Section headings are uppercase and accent-coloured** with a hairline underneath. That is the only heading treatment; do not add another level of visual hierarchy.
- **Hyphenation and justification**: leave text left-aligned, never justified.

## Print rules

Printing to PDF is the primary use, so the print block matters as much as the screen one.

- `@page { size: letter; margin: 0 }` with padding moved into the page container, giving control over margins.
- Force white backgrounds and set `print-color-adjust: exact` so tinted chips survive.
- **Drop to ~10pt** with 1.3 line-height. Screen sizes are too large on paper.
- `break-inside: avoid` on each role, sub-role and the header, so no job entry is split across a page.
- **Hide interactive chrome** — buttons, links styled as controls — in print.

## Accessibility

- Maintain contrast: primary text on white, accent for headings and markers only. Never use the accent for long body text.
- Use real heading elements (`h1`, `h2`) in a sensible order; styling uppercase in CSS rather than typing it in caps.
- Give links descriptive text; do not rely on colour alone to distinguish them.
- Keep the semantic list structure for bullets — screen readers announce list length, which helps on a long CV.

## Anti-patterns

- Multi-column layouts — they break in print and screen readers read them in the wrong order.
- Tables for layout.
- Images or icon fonts in place of text; they do not survive PDF text extraction or ATS parsing.
- Solid accent-filled headers, gradients, drop shadows on content, or decorative rules between every section.
- Headers and footers injected by the browser (date, URL, page count) — disable them in the print dialog.
