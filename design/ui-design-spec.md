# EnergyAtlas Wiki — UI Design Specification

This specification restyles the EnergyAtlas Wiki into the grid-framed, editorial visual language that the BEMGen documentation site and the EnergyAtlas dev-skills site already use. It began as the EnergyAtlas Wiki UI design specification, went to the BEMGen site, and came back here; section 0 records the decisions taken for the Wiki. **Where section 0 and a later section disagree, section 0 wins.**

---

## 0. EnergyAtlas Wiki Implementation Decisions

Decided by the owner on 2026-10-12. These are implementation rules, not one-off clarifications. The guidelines are applied softly: the Wiki has a deeper page hierarchy than the sister sites and its own theme, so section 0 records where it deliberately differs from them.

### 0.1 Brand

- The site stays **EnergyAtlas Wiki**, with its existing logo and favicon (`docs/assets/images/icon.svg`) and the sidebar wordmark "EnergyAtlas Wiki".
- The family resemblance with BEMGen and dev-skills comes from typography, palette, and UI structure.

### 0.2 Sources of truth

- **Reference UI:** the BEMGen documentation site: this document's body, its fonts, and its rendered pages. BEMGen's own reference, a screenshot of the ArtCraft website, is not kept here; section 0.12 describes it.
- **Palette:** this repository. The Wiki's `docs/assets/css/main.css` was the palette source for the sister sites; as of 2026-10-12 it carries the contrast-adjusted tokens of section 0.6, so it stays the source of truth for them.
- **Theme:** the Wiki does not use Material for MkDocs. It has its own MkDocs theme (`theme/base.html`, `theme/main.html`) and stylesheet. Where the body of this document names a Material feature, section 0.14 gives the Wiki's equivalent.

### 0.3 Theme behaviour

- A stored choice (`energyatlas-wiki-theme` in `localStorage`) wins; otherwise the system preference (`prefers-color-scheme`) decides, and dark is used only when the browser cannot report one. The light/dark toggle stays.
- Never force dark mode. A visitor whose system prefers light gets light first.
- Dark mode receives the strongest version of the reference visual language; light mode keeps the same grid, typography, and framing.

### 0.4 Fonts

- Families: **Geist** (primary sans), **Geist Mono** (technical and monospace UI, and code), **Cormorant Garamond** (sparse editorial serif accent, italic). They replace Roboto Flex and Cascadia Code.
- Self-hosted: the Latin and Latin Extended WOFF2 subsets (variable Geist and Geist Mono, Cormorant Garamond italic 500) are copied from the BEMGen documentation site into `docs/assets/fonts/` with their OFL licences, and declared in `docs/assets/css/fonts.css`. The browser contacts no font host; the former Google Fonts import is removed.
- `theme/base.html` preloads `geist-latin.woff2` and `geist-mono-latin.woff2`.

### 0.5 Colour roles

| Role | Dark | Light | Use |
| --- | --- | --- | --- |
| Info / interactive accent | `#4da3ff` | `#125dae` | links, navigation, information, active and selected states, and the accent marks of the subspace icons (section 0.15) |
| Success | `#28a745` | `#188038` | success states |
| Warning | `#ffc107` | `#9a6700` | warnings |
| Error | `#f44336` | `#c5221f` | errors, destructive actions, failures |
| Primary (brand) | `#003978` | `#003978` | deep branded **fill or background** only |

- Red is restricted to error, destructive, and failure states. The former secondary brand red (`#f1392a`, `#c92d22`) is no longer a decorative accent anywhere in the Wiki; the primary-to-red gradient is removed.
- Amber/yellow means warning, green means success, blue means links, navigation, information, and active/selected states.
- `#003978` is never text or a meaningful border on a dark background (1.86:1 on black). Text on a `#003978` fill is white or `#e5e5e5`.
- Syntax highlighting keeps its own palette (Monokai in dark, a light variant in light); it is code colouring, not UI accent.

### 0.6 Contrast

Targets (WCAG 2.2 AA):

- text below 24px (or 18.66px bold), including all 10–12px mono labels: at least 4.5:1 against every surface it sits on;
- large text: at least 3:1;
- borders and edges that convey state or mark an interactive control (inputs, buttons, focus, the active item): at least 3:1;
- decorative grid rules that convey no state may stay lighter.

Adjusted and added tokens:

| Token | Theme | Former Wiki value | Used value | Contrast of used value |
| --- | --- | --- | --- | --- |
| `--ui-text-muted` | dark | `#808080` (4.41:1 on `#1a1a1a`) | `#999999` | 7.37 on `#000000`, 6.11 on `#1a1a1a`, 5.04 on `#2a2a2a` |
| `--ui-text-muted` | light | `#6f7a89` (4.36:1 on white) | `#5f6b7a` | 5.43 on `#ffffff`, 5.05 on `#f4f7fb`, 4.61 on `#e7edf5` |
| `--ui-border-subtle` | dark | `#404040` | `#404040` | decorative grid rules only |
| `--ui-border-subtle` | light | `#cfd8e5` | `#cfd8e5` | decorative grid rules only |
| `--ui-border-interactive` | dark | — | `#6b6b6b` | 3.94 on `#000000`, 3.27 on `#1a1a1a` |
| `--ui-border-interactive` | light | — | `#768599` | 3.76 on `#ffffff`, 3.50 on `#f4f7fb`, 3.19 on `#e7edf5` |

- The tokens use the prefix `--ui-`. `--ea-border` in later sections means `--ui-border-subtle` for grid framing, strips, cells, tables, and code blocks, and `--ui-border-interactive` for inputs, buttons, and other controls; every other `--ea-` token is the `--ui-` token of the same name.
- Focus and active states use the accent colour, which passes everywhere.
- Light-theme success and warning text fall below 4.5:1 on `#e7edf5`; do not set small state-coloured text on the emphasis surface.

### 0.7 Page shell

The Wiki keeps its sidebar shell; it does **not** adopt the sister sites' top header with tabs. Eight subspaces with nested groups do not fit a tab row, and the subspace switcher already solves that navigation.

- **No top header.** The left sidebar holds, top to bottom: the brand row, the subspace switcher, the current subspace's page tree, the development notice, and the tool row (theme toggle, edit this page, GitHub repository, collapse). Each part is separated by a thin horizontal rule, and the sidebar has its own right rule.
- **Subspace switcher:** one full-width row with the subspace icon and its name in Geist bold, normal case; its menu is a flat, square list with thin rules between options, the current option marked by an accent edge and a check.
- **Page tree:** muted Geist labels; the active page in primary text with a 2px accent edge at the left, not a filled block. Groups are collapsible rows with a chevron; nested levels are indented and joined by a thin vertical rule.
- **Tool row:** square 32px controls with interactive borders; the theme toggle is a square two-cell switch (sun, moon) whose active cell is inverted.
- **Frame:** the article and the table of contents sit in a frame of two thin vertical rules, centred in the space to the right of the sidebar, with empty margins outside it. Where the frame fills that space, its left rule and the sidebar's rule fall on the same pixel column and read as one line. The table of contents sits in its own column behind a thin vertical rule.
- **Collapse and drawer:** the desktop collapse control and the below-1081px drawer stay as they work today; both become square and flat (no drop shadows, no blur behind the drawer).
- **Scroll progress:** a 2px accent rule along the bottom edge of the window.
- **Development notice:** the "WIP EnergyAtlas Wiki" message appears twice. Until it is dismissed, it is a floating window at the bottom right: square, flat, a mono uppercase title bar, the message, and a square button. It also sits permanently at the bottom of the sidebar, above the tool row, with a mono uppercase title like the other sidebar labels.

### 0.8 Welcome page

The site root keeps redirecting to Quick Start › Welcome (`quick-start/index.md`). The Welcome page carries the hero; there is no separate landing page.

- Order: hero, the cover screenshot, the `Subspaces` strip with a shared-border grid of the eight subspaces (cells `A`–`H`, each linking to the subspace's first page), then the existing content with strips on its `##` headings.
- Headline, on two lines:

  ```text
  EnergyAtlas
  agentic digital twins for city-scale energy insights.
  ```

  `EnergyAtlas` in Geist; the second line in Cormorant Garamond italic. Supporting copy is one or two sentences.
- The headline is sized to the hero's width (container query units), so the serif line takes at most two lines on desktop.
- The Welcome page keeps both sidebars; no hidden-sidebar insets are needed.
- No oversized CTAs, imagery beyond the existing cover, or animation.

### 0.9 Numbered section strips

Strips (`01 / OVERVIEW`, section 7) are turned on per page with the front-matter flag `overview: true`. They then number every `##` heading of that page automatically, keeping its text and anchor; an optional right-hand annotation comes from the heading's `data-note` attribute (`## Title {data-note="Model pipeline"}`).

They are on:

- the Welcome page and the subspace overview pages: Workflows, Architecture, Library, User Stories;
- the section index pages of nested groups: Shading Guides, the Web API Development Guide, and Web Development.

They are not on ordinary pages, the Wiki Guide (its `##` headings include Markdown examples), the object reference, or the generated Python and Web API references.

### 0.10 Content width

- Long-form prose (paragraphs, lists, block quotes, headings) is capped at 52rem (832px) inside the article column.
- Exempt, using the full article column (up to 960px): tables, code blocks, images, Plotly charts, diagrams, strips, and grids. Pages with `full_width: true` (the Architecture subspace) have no prose cap.
- Wide tables sit in a bounded horizontal-scrolling container; the page viewport itself must never overflow horizontally.

### 0.11 Breadcrumbs

- Breadcrumbs show the page's full ancestry in the navigation (subspace, then every group), not only the first two levels.
- Restrained technical style: small uppercase Geist Mono, muted colour, `/` separators in the same colour, no bar, background, or border.

### 0.12 The reference screenshot, described

What the BEMGen site took from the ArtCraft reference, and what the Wiki takes from it in turn:

- **Surface:** near-black page background; content in off-white, secondary text in mid-grey.
- **Page frame:** the content column is bounded by two full-height vertical rules, with empty margins outside them. Horizontal rules run between sections and meet the frame.
- **Header:** low, one line, thin bottom rule; nav labels in small uppercase, widely tracked monospace. The active item is a small inverted block inside a thin blue rectangular outline. (The Wiki applies this treatment to its sidebar rows rather than a header, section 0.7.)
- **Section strip:** about 48px high between two horizontal rules: `02 / OWNERSHIP` at the left and a right-aligned annotation at the right, both small, uppercase, tracked mono, muted.
- **Hero cell:** generous padding and empty space; a large, very bold sans headline with tight leading, a phrase set in a serif italic; one short supporting paragraph in grey, roughly 60 characters wide.
- **Feature row:** equal cells sharing their borders. Each cell: a one-letter mono index (`A`, `B`, `C`) at the top left in muted grey, a bold title, two lines of grey description, and optionally a small square outlined button with a mono uppercase label.
- **Not adopted:** the right-hand scroll ruler with tick numbers and percentage, the oversized outline section names in the right margin, and the `+` registration marks. They are page-specific decoration and conflict with section 19.

### 0.13 Grid cells

- A cell whose title is a link is clickable as a whole and goes to the title's address; hovering it shifts the surface and turns the title blue. Other links in the cell keep their own targets.
- A cell's text is padded by the same gutter as the strip labels, so cell text and strip labels share one left edge.
- Every cell is closed on all four sides.
- Markup: `md_in_html` is enabled; a grid is `<div class="ui-grid" markdown>` around a Markdown list whose items start with a linked title.
- **Icon cards** (`<div class="ui-grid ui-cards" markdown>`, the Welcome page's subspace grid; decided 2026-10-12): no letter index; each item starts with `<span class="ui-icon" data-icon="<slug>"></span>` before its linked title, which `hooks/icons.py` replaces with the subspace icon, shown above the title at 2.5rem; the description is one short line. On hover or focus the card fills with a soft accent gradient (transparent at the upper left to 16% accent at the lower right) and shows a faint (14%) copy of its icon in the accent colour, 1.05 times the card's width, centred at 70% across and 72% down the card and cropped by it. This hover wash is the one deliberate exception to "no decorative gradients" (section 5).

### 0.14 Material features and their Wiki equivalents

| Body of this document | EnergyAtlas Wiki |
| --- | --- |
| Header and tabs (sections 9.1, 21) | Sidebar brand row and subspace switcher (section 0.7) |
| `navigation.path` breadcrumbs | `theme/main.html` breadcrumbs from `page.ancestors` (section 0.11) |
| `navigation.instant` | Not available. Page changes stay stable through preloaded fonts, `scrollbar-gutter: stable`, and removing the former content fade-out and fade-in on every navigation. |
| `slate` / `default` schemes | `:root` (dark) and `:root[data-theme="light"]` |
| Admonitions (section 14) | The Wiki does not enable admonitions; block quotes take the panel treatment. |
| Search (section 15) | The Wiki has no search interface; none is added in this redesign. |
| `grid cards` | `ui-grid` (section 0.13) |


### 0.15 Subspace icons

Decided by the owner on 2026-10-12. The eight subspace icons are a hand-drawn family that replaces the former Lucide and Simple Icons glyphs.

- **Style:** restrained editorial line drawings: ink in slightly irregular, gently tapering strokes, minimal detail, generous negative space, and one accent mark per icon in the theme's accent blue (decided 2026-10-12, replacing the first draft's terracotta). No gradients, shadows, scribble fills, or geometric icon-kit construction.
- **Subjects:** Quick Start, a compass with an accent needle; Workflows, a node, a curved arrow, and an accent node (redrawn 2026-10-12); Architecture, three blocks on branching lines, one accented; Python, the language's logo of two interlocking snakes, the upper in ink and the lower in the accent (redrawn 2026-10-12); WebAPI, `< / >` with an accent slash; Library, two upright books, one accented, and one leaning; User Stories, a figure and an accent speech bubble; Wiki Guide, an open book with an accent ribbon.
- **Weights:** two weights of the same drawings: regular (`<slug>.svg`, stroke 1.3 of 24) for large display on the Welcome cards, and bold (`<slug>-bold.svg`, stroke 1.85 of 24) for the sidebar, where the regular line reads too thin.
- **Files:** `theme/icons/subspaces/<slug>.svg` and `<slug>-bold.svg`, each on a 24x24 canvas with a transparent background, its ink in a `.ink` group (warm charcoal `#3b3631` in the file) and its accent in an `.accent` group (`#125dae` in the file). They are generated by `design/icons/generate_subspace_icons.py` (seeded, so reruns are identical); edit the generator, not the SVGs.
- **On the site:** inlined, so CSS sets their colours: the ink takes the colour of the surrounding text (`currentColor`), the accent takes `--ui-accent`, so both follow the theme. Sizes: 26px in the subspace switcher and its menu, 20px elsewhere in the sidebar, 2.5rem on the Welcome page's icon cards (section 0.13).

---

## 1. Design Intent

Restyle the MkDocs website using the reference UI (section 0.2) as the primary visual reference for:

- grid structure
- border framing
- typography hierarchy
- card construction
- spacing
- navigation character
- technical/editorial tone

Use the existing **EnergyAtlas Wiki** as the source of truth for brand colors and documentation behavior.

The result should feel:

- technical
- editorial
- architectural
- precise
- minimal
- engineering-oriented
- documentation-first

The design should avoid generic SaaS or stock Material Design patterns.

---

## 2. Visual Priorities

Use the following order of precedence:

1. **Reference UI**
   - framing
   - borders
   - page grid
   - content cells
   - typography hierarchy
   - section indexing
   - navigation treatment
   - spacing

2. **Existing EnergyAtlas Wiki**
   - brand colors
   - light/dark theme palette
   - information architecture
   - documentation structure
   - semantic state colors

3. **Typography**
   - Geist for primary UI and documentation text
   - Geist Mono for technical labels and metadata
   - Cormorant for occasional editorial emphasis

The goal is not to reproduce another site literally. The goal is to transfer its disciplined, grid-based design language into EnergyAtlas.

---

# 3. Typography

## 3.1 Primary Sans Serif

Use **Geist** as the primary typeface across the interface.

Use Geist for:

- page headings
- body text
- navigation
- sidebar
- cards
- buttons
- tables
- search
- captions
- labels where monospacing is not required

Recommended fallback:

```css
font-family: "Geist", "Inter", "Helvetica Neue", Arial, sans-serif;
```

### Heading behavior

Headings should rely on weight, spacing, and scale rather than decorative styling.

Recommended characteristics:

```css
font-weight: 650 750;
line-height: 0.95 1.15;
letter-spacing: -0.02em;
```

Suggested display sizes:

```css
display-xl: 64px;
display-lg: 56px;
display-md: 48px;

h1: 40px;
h2: 30px;
h3: 22px;
h4: 18px;
```

Documentation headings should scale down appropriately on smaller screens.

### Body text

Recommended baseline:

```css
font-size: 16px;
line-height: 1.6;
font-weight: 400;
```

For introductory or prominent body copy:

```css
font-size: 18px;
line-height: 1.6;
```

Use secondary text colors rather than pure white for long-form content.

---

## 3.2 Technical Labels

Use **Geist Mono** where available.

Recommended fallback:

```css
font-family: "Geist Mono", "IBM Plex Mono", Consolas, monospace;
```

Use for:

- section indices
- page metadata
- card labels
- breadcrumbs
- small navigation labels
- technical annotations
- code-adjacent UI
- compact buttons

Recommended treatment:

```css
font-size: 10px 12px;
font-weight: 550 650;
text-transform: uppercase;
letter-spacing: 0.12em 0.16em;
```

Examples:

```text
01 / QUICK START
02 / WORKFLOWS
A
B
C
SYSTEM OVERVIEW
MODEL PIPELINE
```

---

## 3.3 Editorial Serif

Use **Cormorant** or **Cormorant Garamond** for occasional editorial emphasis.

Prefer the Google Fonts version when available.

Use it only for selective phrases in large display headings.

Example (the Wiki's Welcome headline, section 0.8):

```text
EnergyAtlas
agentic digital twins for city-scale energy insights.
```

The second line uses Cormorant italic while `EnergyAtlas` remains Geist.

Do not use Cormorant for:

- body copy
- navigation
- tables
- standard documentation headings
- buttons
- sidebars

It should function as a restrained editorial accent.

---

# 4. Color System

Use the existing EnergyAtlas palette as the source of truth: the Wiki's `docs/assets/css/main.css` (section 0.2), with the contrast adjustments of section 0.6. The blocks below already include those adjustments.

## 4.1 Dark Theme

```css
--ea-primary:            #003978;  /* deep branded fill only */
--ea-accent:             #4da3ff;

--ea-text-primary:       #e5e5e5;
--ea-text-secondary:     #b0b0b0;
--ea-text-muted:         #999999;  /* wiki: #808080; adjusted, section 0.6 */

--ea-bg-base:            #000000;
--ea-bg-surface-1:       #1a1a1a;
--ea-bg-surface-2:       #2a2a2a;
--ea-bg-surface-3:       #3a3a3a;

--ea-border-subtle:      #404040;  /* decorative grid rules */
--ea-border-interactive: #6b6b6b;  /* controls; added, section 0.6 */

--ea-success:            #28a745;
--ea-warning:            #ffc107;
--ea-error:              #f44336;  /* wiki --secondary-color #f1392a is not used as an accent */
```

### Dark theme usage

- Base page background: `#000000`
- Primary surfaces: `#1a1a1a`
- Secondary surfaces: `#2a2a2a`
- Higher-emphasis surfaces: `#3a3a3a`
- Main text: `#e5e5e5`
- Secondary text: `#b0b0b0`
- Metadata: `#999999`
- Grid borders: `#404040`; control borders: `#6b6b6b`
- Main interaction accent: `#4da3ff`
- Deep branded fill: `#003978` (never text on dark)
- Red only for error, destructive, and failure states (section 0.5)

The interface should remain predominantly monochromatic. Accent colors should be used sparingly.

---

## 4.2 Light Theme

```css
--ea-primary:            #003978;  /* deep branded fill only */
--ea-accent:             #125dae;

--ea-text-primary:       #18202c;
--ea-text-secondary:     #3f4b5b;
--ea-text-muted:         #5f6b7a;  /* wiki: #6f7a89; adjusted, section 0.6 */

--ea-bg-base:            #ffffff;
--ea-bg-surface-1:       #f8fafc;  /* wiki --bg-gradient-dark ("subtle") */
--ea-bg-surface-2:       #f4f7fb;  /* wiki --bg-light ("surface") */
--ea-bg-surface-3:       #e7edf5;  /* wiki --bg-dark-surface ("emphasis") */

--ea-border-subtle:      #cfd8e5;  /* decorative grid rules */
--ea-border-interactive: #768599;  /* controls; added, section 0.6 */

--ea-success:            #188038;
--ea-warning:            #9a6700;
--ea-error:              #c5221f;  /* wiki --secondary-color #c92d22 is not used as an accent */
```

The light surfaces use the same token names as the dark ones, in the same order of emphasis, so components never branch on the theme.

The light theme should preserve the same grid structure, typography hierarchy, and flat framing as the dark theme.

The dark theme should be the stronger expression of the design language.

---

# 5. Core Layout System

The page should be organized around a **continuous rectilinear grid**.

Primary characteristics:

- thin horizontal rules
- thin vertical rules
- aligned content cells
- shared borders
- strong column discipline
- deliberate whitespace
- flat surfaces
- square corners

Recommended base treatment:

```css
border: 1px solid var(--ea-border);
border-radius: 0;
box-shadow: none;
```

Avoid:

- rounded cards
- pills
- floating cards
- decorative gradients
- glassmorphism
- drop shadows
- large icon tiles
- disconnected feature boxes
- excessive use of colored fills

The interface should read as one structured document rather than a collection of independent components.

---

# 6. Grid Framing

Major sections should be aligned to the same page-wide grid.

Prefer shared borders between adjacent cells.

Example:

```text
┌──────────────────────────────────────────────────────┐
│ 02 / WORKFLOWS                      MODEL PIPELINE   │
├──────────────────┬──────────────────┬────────────────┤
│ A                │ B                │ C              │
│                  │                  │                │
│ Urban Data       │ Simulation       │ Results        │
│ ...              │ ...              │ ...            │
│                  │                  │                │
└──────────────────┴──────────────────┴────────────────┘
```

This is preferred over three visually isolated cards.

The grid should create continuity across the page.

---

# 7. Section Headers

Use thin section-index strips for major content areas, on the pages listed in section 0.9 only.

Example:

```text
02 / WORKFLOWS                              MODEL PIPELINE
```

Recommended characteristics:

```css
height: 40px 48px;
border-top: 1px solid var(--ea-border);
border-bottom: 1px solid var(--ea-border);
```

Typography:

```css
font-family: "Geist Mono", monospace;
font-size: 10px 12px;
font-weight: 600;
letter-spacing: 0.14em;
text-transform: uppercase;
```

Use muted text colors.

These strips should feel like:

- technical drawing annotations
- engineering document indexing
- sheet metadata
- system labels

They should not resemble marketing section headers.

---

# 8. Feature Cards

Feature cards should behave as **grid cells**.

Recommended structure:

```text
A

Urban Data Integration
Import and prepare geospatial building datasets.

[ VIEW WORKFLOW ]
```

Recommended styling:

```css
padding: 28px 36px;
background: transparent;
border-radius: 0;
box-shadow: none;
```

Title:

```css
font-family: "Geist", sans-serif;
font-weight: 650 700;
font-size: 24px 28px;
```

Description:

```css
font-family: "Geist", sans-serif;
font-size: 16px;
line-height: 1.55;
color: var(--ea-text-secondary);
```

Card identifier:

```css
font-family: "Geist Mono", monospace;
font-size: 10px 11px;
letter-spacing: 0.14em;
color: var(--ea-text-muted);
```

Hover state:

- slightly brighter border
- slight surface shift
- optional blue title or micro-accent
- no translate animation
- no shadow elevation

---

# 9. Navigation

## 9.1 Top Navigation

The top navigation should be compact and linear.

Recommended characteristics:

- dark background
- thin bottom border
- low vertical height
- small technical typography
- strong horizontal alignment

Navigation labels:

```css
font-family: "Geist Mono", monospace;
font-size: 11px 13px;
font-weight: 600;
letter-spacing: 0.08em 0.14em;
text-transform: uppercase;
```

Active states may use:

- brighter text
- thin bottom rule
- subtle blue outline
- small blue edge
- restrained rectangular selection

Avoid rounded tabs.

---

## 9.2 Sidebar

The sidebar should remain functional and documentation-first.

Use:

- near-black or transparent background
- thin vertical divider
- muted inactive labels
- off-white active label
- blue accent for active state
- restrained indentation
- flat nested navigation

Avoid filled Material-style active blocks.

Hierarchy should come from:

- spacing
- indentation
- typography
- muted color changes
- thin rules

---

# 10. Buttons

Buttons should feel like compact technical controls.

Recommended base:

```css
background: transparent;
border: 1px solid var(--ea-border-interactive);
border-radius: 0;
box-shadow: none;
```

Typography:

```css
font-family: "Geist Mono", monospace;
font-size: 10px 12px;
font-weight: 600;
letter-spacing: 0.08em 0.12em;
text-transform: uppercase;
```

Hover states may:

- brighten the border
- use `#4da3ff`
- invert foreground/background for primary actions

Avoid oversized CTA styling.

---

# 11. Documentation Content

Long-form documentation should remain highly readable.

Recommended article width:

```css
max-width: 760px 900px;
```

This width is for long-form prose only. Reference pages, large diagrams, data matrices, and wide tables are exempt, and wide tables scroll inside a bounded container (section 0.10).

Use generous vertical rhythm.

Suggested section spacing:

```css
h1 margin-top: 0;
h2 margin-top: 64px;
h3 margin-top: 40px;
paragraph margin-bottom: 1.25em;
```

Do not force every content block into a bordered container.

The page shell should provide structure; prose should remain visually open.

---

# 12. Tables

Tables should follow the same technical grid language.

Recommended characteristics:

- square outer edges
- thin row and column rules
- flat background
- no rounded outer wrapper
- subtle hover state
- restrained header styling
- blue only for interaction or selected states

Recommended header treatment:

```css
font-family: "Geist Mono", monospace;
font-size: 11px;
font-weight: 600;
letter-spacing: 0.08em;
text-transform: uppercase;
```

Tables should feel closer to technical data sheets than application widgets.

---

# 13. Code

Use **Geist Mono** where possible.

Code block base:

```css
background: var(--ea-bg-surface-1);
border: 1px solid var(--ea-border);
border-radius: 0;
box-shadow: none;
```

Inline code should be understated.

Avoid pill-shaped inline code.

Recommended inline treatment:

```css
background: var(--ea-bg-surface-1);
padding: 0.1em 0.3em;
border-radius: 0;
```

---

# 14. Admonitions and Callouts

Admonitions should feel like technical panels rather than colorful Material cards.

Example:

```text
NOTE
────────────────────────────────────
Content...
```

Recommended styling:

- square edges
- thin outer rule or leading rule
- small mono heading
- low-contrast surface
- restrained semantic accents

Semantic colors may appear in:

- a thin edge
- small heading
- compact icon
- label text

Avoid large saturated background fills.

---

# 15. Search

Search should match the same technical language.

Use:

- square input geometry
- thin borders in `--ea-border-interactive`
- near-black or white surface depending on theme
- Geist text
- Geist Mono for metadata or keyboard hints
- no floating shadow-heavy search modal

Focus state:

```css
border-color: var(--ea-accent);
outline: none;
```

---

# 16. Spacing System

Recommended spacing scale:

```css
--space-xs:   4px;
--space-sm:   8px;
--space-md:  16px;
--space-lg:  24px;
--space-xl:  32px;
--space-2xl: 48px;
--space-3xl: 64px;
```

Typical usage:

- section strips: compact
- cards: `28px 36px`
- article sections: `40px 64px`
- hero regions: `48px 64px`
- navigation: compact
- sidebars: dense but not cramped

---

# 17. Hero / Landing Page Areas

Landing-page hero sections may use larger scale typography and more negative space.

Recommended characteristics:

```css
padding-top: 64px;
padding-bottom: 72px;
```

Display heading:

```css
font-size: 48px 64px;
line-height: 0.98 1.05;
font-weight: 700;
letter-spacing: -0.03em;
```

Use Cormorant italic selectively within the heading if editorial emphasis is desirable.

The Wiki's headline (section 0.8):

```text
EnergyAtlas
agentic digital twins for city-scale energy insights.
```

Treatment:

- `EnergyAtlas` — Geist
- `agentic digital twins for city-scale energy insights.` — Cormorant Garamond italic

Use sparingly. The hero stays restrained and is followed immediately by the shared-border grid.

---

# 18. Borders

Borders are one of the main visual devices.

Use them deliberately.

Recommended default:

```css
border-color: var(--ea-border);
border-width: 1px;
```

Where lower contrast is appropriate:

```css
border-color: color-mix(
  in srgb,
  var(--ea-border) 65%,
  transparent
);
```

Borders should define structure, not decorate every element independently.

Prefer continuous alignment across sections.

---

# 19. Motion

Animation should be minimal.

Allowed:

- subtle color transitions
- border changes
- opacity changes
- small underline or line expansion

Recommended timing:

```css
transition: 120ms 180ms ease;
```

Avoid:

- card lifting
- parallax
- bounce
- large scaling
- exaggerated hover motion
- continuous decorative animation

---

# 20. Responsive Behavior

## Desktop

- 2–3 column content grids
- persistent sidebar where useful
- strong horizontal alignment
- visible shared borders
- wider technical section strips

## Tablet

- reduce 3-column grids to 2 columns
- preserve border continuity
- slightly reduce padding
- maintain typography hierarchy

## Mobile

- stack cells vertically
- preserve square corners
- retain horizontal rules
- collapse navigation conventionally
- keep technical labels compact
- avoid introducing separate mobile card styling

The visual language should remain consistent at all breakpoints.

---

# 21. MkDocs-Specific Guidance

Override the default appearance enough that the result no longer reads as stock MkDocs or stock Material Design.

Priority components:

- header
- sidebar
- page TOC
- search
- tables
- code blocks
- admonitions
- tabs
- navigation states
- content cards
- pagination
- breadcrumbs

Retain MkDocs usability while replacing the default component styling with the EnergyAtlas grid system.

---

# 22. Theme Implementation Guidance

Recommended CSS token structure:

```css
:root {
  --font-sans: "Geist", "Inter", "Helvetica Neue", Arial, sans-serif;
  --font-mono: "Geist Mono", "IBM Plex Mono", Consolas, monospace;
  --font-serif: "Cormorant Garamond", "Cormorant", Georgia, serif;

  --ea-primary: #003978;
  --ea-accent: #4da3ff;

  --ea-text-primary: #e5e5e5;
  --ea-text-secondary: #b0b0b0;
  --ea-text-muted: #999999;

  --ea-bg-base: #000000;
  --ea-bg-surface-1: #1a1a1a;
  --ea-bg-surface-2: #2a2a2a;
  --ea-bg-surface-3: #3a3a3a;

  --ea-border-subtle: #404040;
  --ea-border-interactive: #6b6b6b;

  --ea-success: #28a745;
  --ea-warning: #ffc107;
  --ea-error: #f44336;

  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 48px;
  --space-3xl: 64px;

  --radius: 0;
  --shadow: none;
}
```

For light mode, swap the color tokens (section 4.2) while preserving structure. Which set applies follows `data-theme` on the root element (`:root` for dark, `:root[data-theme="light"]` for light), chosen by the stored choice, the system preference, and the toggle (section 0.3).

---

# 23. Component Principles

Every component should satisfy the following:

1. **Flat**
   - no visual elevation unless absolutely necessary

2. **Aligned**
   - follows shared page columns and rules

3. **Square**
   - no soft card geometry

4. **Restrained**
   - limited color and motion

5. **Typographic**
   - hierarchy comes mainly from type

6. **Technical**
   - labels and metadata should feel precise

7. **Integrated**
   - components should feel like part of one system rather than isolated widgets

---

# 24. Final Visual Character

The completed site should feel like a combination of:

- technical documentation
- architectural drawing set
- engineering interface
- research publication
- high-end developer documentation

It should remain unmistakably EnergyAtlas through its palette and information architecture, while adopting a more disciplined, grid-based, editorial visual system.

The final design should prioritize:

- structure over decoration
- typography over iconography
- borders over shadows
- alignment over ornament
- information hierarchy over visual novelty
