# LifeQuest — Component Library

> **Canonical source:** This document defines every reusable UI component in the LifeQuest project.  
> **Priority:** `design_tokens.json` > `ui_style.md` > `components.md` (this file).  
> **AI agents:** Before creating a new component, check if an existing one can be extended. Before modifying a component, update this document.

---

## Table of Contents

1. [Component Usage Rules](#1-component-usage-rules)
2. [Button](#2-button)
3. [FormInput / FormField](#3-forminput--formfield)
4. [CharacterCard](#4-charactercard)
5. [GamePanel](#5-gamepanel)
6. [WoodSign](#6-woodsign)
7. [Message](#7-message)
8. [LoadingOverlay](#8-loadingoverlay)
9. [Screen](#9-screen)
10. [PixelScene](#10-pixelseene)
11. [Modal](#11-modal)
12. [Avatar](#12-avatar)
13. [ProgressBar](#13-progressbar)
14. [Quick Reference](#14-quick-reference)

---

## 1. Component Usage Rules

1. **Use existing components** — never build a new visual element from scratch if a component already covers it.
2. **Component variants** — use CSS class modifiers (`.btn--disabled`, `.panel--collapsed`) to create variants; never duplicate HTML.
3. **Slot system** — components accept content via named containers (e.g. `.panel-title` + `.panel-content`). Follow the HTML examples exactly.
4. **No inline styles** — all visual properties must come from CSS classes or CSS custom properties.
5. **Responsive** — every component must work at 320px minimum width.
6. **Reduced motion** — every animated component must respect `prefers-reduced-motion: reduce`.
7. **No JS logic in CSS** — JavaScript-driven state changes use class toggling (`.active`, `.disabled`, `.loading`), never inline style manipulation for layout.

---

## 2. Button

### Purpose

A reusable action button with two visual contexts (dark UI and wood sign) and three semantic variants (primary, success, secondary).

### HTML Structure

```html
<button class="btn btn-primary" onclick="..." aria-label="...">
    Submit
</button>
```

### CSS Classes

| Class | Context | Purpose |
|-------|---------|---------|
| `.btn` | Universal | Base button styles (padding, font, border, transition, active press) |
| `.btn-primary` | All | Primary action — danger/delete/emphasis |
| `.btn-success` | All | Confirm/save/positive action |
| `.btn-secondary` | All | Cancel/back/secondary/dismiss |
| `.btn:disabled` | All | Disabled state (`opacity: 0.6`, `cursor: not-allowed`) |
| `.btn:active` | All | Press effect (`transform: scale(0.98)` or `translateY(3px)`) |

### Context Switching

The same `.btn` classes work in **two visual contexts** automatically via CSS scoping:

**Dark UI context** (inside `.game-screen`, `.dashboard-screen`):
- `background: transparent`
- `border: 2px solid currentColor`
- `border-radius: 4px`
- Hover adds `background-color: rgba(...)` + `box-shadow` glow
- No 3D shadow

**Wood sign context** (inside `.wood-sign`):
- `border: 3px solid var(--wood-edge)`
- `border-radius: 0`
- 3D press effect via `box-shadow` + `translateY(3px)` on active
- Colored gradient backgrounds:
  - `.btn-primary` → green gradient (`#6a9a40` → `#4a7a28`)
  - `.btn-success` → gold gradient (`#c89030` → `#a07020`)
  - `.btn-secondary` → transparent cream (`rgba(255, 248, 230, 0.6)`)

### Dimensions

| Property | Dark UI | Wood Sign |
|----------|---------|-----------|
| Padding | `12px 20px` | `14px 12px` |
| Min touch target | 44×44px | 44×44px |
| Border radius | `4px` | `0` |
| Border width | `2px` | `3px` |
| Width | `100%` (full-width in forms) | `100%` (full-width in signs) |

### Colors

| Variant | Dark UI Text | Dark UI Hover Bg | Wood Sign Bg | Wood Sign Hover Bg |
|---------|-------------|------------------|-------------|-------------------|
| Primary | `--accent-red` (`#e94560`) | `rgba(233, 69, 96, 0.2)` | `linear-gradient(180deg, #6a9a40, #4a7a28)` | `linear-gradient(180deg, #7aaa50, #5a8a38)` |
| Success | `--accent-gold` (`#d4af37`) | `rgba(212, 175, 55, 0.2)` | `linear-gradient(180deg, #c89030, #a07020)` | `linear-gradient(180deg, #d8a040, #b08030)` |
| Secondary | `--text-secondary` (`#808080`) | `--text-primary` + `box-shadow` | `rgba(255, 248, 230, 0.6)` | `rgba(255, 248, 230, 0.9)` |

### Shadow Tokens

Refer to `design_tokens.json` → `shadow` → `btnPrimaryHover`, `woodSignBtnPrimary`, `woodSignBtnPrimaryHover`, etc.

| Button | Default Shadow | Hover Shadow |
|--------|---------------|--------------|
| Dark UI primary | none | `0 0 15px rgba(233, 69, 96, 0.4)` |
| Dark UI success | none | `0 0 15px rgba(212, 175, 55, 0.4)` |
| Dark UI secondary | none | `0 0 10px rgba(192, 192, 192, 0.3)` |
| Wood primary | `0 4px 0 #2a5018, 0 6px 12px rgba(0,0,0,0.3)` | `0 4px 0 #2a5018, 0 8px 16px rgba(0,0,0,0.35)` |
| Wood success | `0 4px 0 #604010, 0 6px 12px rgba(0,0,0,0.3)` | `0 4px 0 #604010, 0 8px 16px rgba(0,0,0,0.35)` |
| Wood secondary | `0 3px 0 #6b4423` | `0 3px 0 #6b4423, 0 5px 10px rgba(0,0,0,0.2)` |

### Animations

| State | Duration | Effect |
|-------|----------|--------|
| Hover (all) | `0.3s ease` | Background + shadow transition |
| Active (dark UI) | `0.1s` | `transform: scale(0.98)` |
| Active (wood sign) | `0.1s` | `transform: translateY(3px)`; shadow reduces to `0 1px 0 var(--wood-edge)` |

### Behaviour

- **Disabled:** `opacity: 0.6`, `cursor: not-allowed`, no hover glow, no active transform.
- **Loading:** Add class `.loading` to button → `opacity: 0.6`, `pointer-events: none`.
- **Icons inside buttons:** Never add icons (see Icon Usage Rules in `ui_style.md`).
- **Text:** 1–2 words max. Uppercase, `letter-spacing: 1px`.

### Variants

| Variant | Class Combo | Context | Use Case |
|---------|-------------|---------|----------|
| Dark UI Primary | `btn btn-primary` (no extra class) | `.game-screen`, `.dashboard-screen` | Main CTA, delete, danger |
| Dark UI Success | `btn btn-success` | `.game-screen`, `.dashboard-screen` | Confirm, save |
| Dark UI Secondary | `btn btn-secondary` | `.game-screen`, `.dashboard-screen` | Cancel, back |
| Wood Primary | `btn btn-primary` inside `.wood-sign` | Sign menus | "New Game", "Submit" |
| Wood Success | `btn btn-success` inside `.wood-sign` | Sign menus | "Continue", "Save" |
| Wood Secondary | `btn btn-secondary` inside `.wood-sign` | Sign menus | "Back", "Cancel" |

### Examples

```html
<!-- Dark UI primary button -->
<button class="btn btn-primary" onclick="submitForm()">Submit</button>

<!-- Wood sign success button -->
<div class="wood-sign">
    <button class="btn btn-success" onclick="continueGame()">Continue</button>
</div>

<!-- Disabled button -->
<button class="btn btn-primary" disabled>Save</button>

<!-- Loading button -->
<button class="btn btn-primary loading" onclick="save()">Saving...</button>
```

### Source

**CSS:** `frontend/css/main.css` — `.btn`, `.btn-primary`, `.btn-success`, `.btn-secondary`, `.btn:active`, `.btn:disabled`  
**CSS:** `frontend/css/pixel-scene.css` — `.wood-sign .btn`, `.wood-sign .btn-primary`, `.wood-sign .btn-success`, `.wood-sign .btn-secondary`  
**JS:** `frontend/js/dashboard.js` — uses buttons for navigation

---

## 3. FormInput / FormField

### Purpose

Text input field with label, hint, and contextual styling for both dark UI and wood sign environments.

### HTML Structure

```html
<div class="form-group">
    <label class="form-label" for="field-id">Field Label</label>
    <input
        type="text"
        id="field-id"
        class="form-input"
        placeholder="Enter value..."
        aria-describedby="field-id-hint"
    />
    <span class="form-hint" id="field-id-hint">Optional hint text</span>
</div>
```

### CSS Classes

| Class | Purpose |
|-------|---------|
| `.form-group` | Wrapper — `margin-bottom: 15px` |
| `.form-label` | Label — uppercase, `--accent-gold`, bold |
| `.form-input` | Input element — dark bg, monospace, 2px border |
| `.form-hint` | Hint text — `--text-secondary`, `12px` |
| `.pixel-input` | Optional — ensures pixel font on non-wood-sign inputs |

### Context Switching

**Dark UI context** (outside `.wood-sign`):
- `background: var(--secondary-dark)` (`#16213e`)
- `border: 2px solid var(--border-color)` (`#404854`)
- `border-radius: 4px`
- `color: var(--text-primary)`
- Focus: `border-color: var(--accent-gold)`, `box-shadow: 0 0 10px rgba(212, 175, 55, 0.3)`

**Wood sign context** (inside `.wood-sign`):
- `background: rgba(255, 248, 230, 0.85)` (cream paper)
- `border: 3px solid var(--wood-dark)` (`#6b4423`)
- `border-radius: 0` (pixel-perfect)
- `color: var(--wood-edge)`
- `box-shadow: inset 2px 2px 0 rgba(0,0,0,0.08), 0 3px 0 var(--wood-edge)`
- Focus: `background: #fff8e8`, gold outline via `box-shadow`

### Dimensions

| Property | Dark UI | Wood Sign |
|----------|---------|-----------|
| Padding | `10px 12px` | `12px 10px` |
| Border radius | `4px` | `0` |
| Border width | `2px` | `3px` |
| Width | `100%` | `100%` |
| Font | 14px monospace | `clamp(8px, 2vw, 10px)` pixel font |

### Behaviour

- **Focus:** `outline: none` + gold border/shadow glow
- **Disabled:** `opacity: 0.6`, `cursor: not-allowed`
- **Error state:** Add `border-color: var(--error)` via JS
- **Placeholder:** `--text-secondary` (dark UI) or `rgba(107, 68, 35, 0.45)` (wood sign)
- **Transition:** `all 0.3s ease`

### Variants

| Variant | Classes | Notes |
|---------|---------|-------|
| Standard text | `form-input` | Default monospace input |
| Pixel input | `form-input pixel-input` | Ensures pixel font outside wood sign |
| Disabled | `form-input[disabled]` | Grayed out, non-interactive |

### Examples

```html
<!-- Dark UI input with label -->
<div class="form-group">
    <label class="form-label" for="username">Username</label>
    <input type="text" id="username" class="form-input" placeholder="Enter name" />
    <span class="form-hint">3-20 characters, letters and numbers</span>
</div>

<!-- Wood sign input -->
<div class="wood-sign">
    <div class="form-group">
        <label class="form-label" for="password">Password</label>
        <input type="password" id="password" class="form-input" placeholder="••••••••" />
    </div>
</div>
```

### Source

**CSS:** `frontend/css/main.css` — `.form-group`, `.form-label`, `.form-input`, `.form-hint`  
**CSS:** `frontend/css/pixel-scene.css` — `.wood-sign .form-label`, `.wood-sign .form-input`, `.wood-sign .form-hint`  
**HTML:** `frontend/index.html` — (future forms will use this pattern)

---

## 4. CharacterCard

### Purpose

Read-only display of a player character's key stats in a compact, bordered card. Used in the dashboard screen.

### HTML Structure

```html
<div class="character-card">
    <div class="stat-row">
        <span class="stat-label">Name</span>
        <span class="stat-value" id="player-name">—</span>
    </div>
    <div class="stat-row">
        <span class="stat-label">Level</span>
        <span class="stat-value" id="player-level">—</span>
    </div>
    <!-- ... more stat rows ... -->
</div>
```

### CSS Classes

| Class | Purpose |
|-------|---------|
| `.character-card` | Card wrapper — semi-transparent dark bg, border, padding |
| `.stat-row` | Row — flex row, bottom border separator, last-child no border |
| `.stat-label` | Label — `--text-secondary`, uppercase, `14px` |
| `.stat-value` | Value — `--accent-gold`, bold, monospace, `16px` |

### Dimensions

| Property | Value |
|----------|-------|
| Padding (card) | `15px 20px` |
| Gap between rows | `8px` (via `padding: 8px 0`) |
| Border radius | `4px` |
| Border | `1px solid var(--border-color)` |
| Background | `rgba(22, 33, 62, 0.5)` |

### Colors

| Element | Color |
|---------|-------|
| Card background | `rgba(22, 33, 62, 0.5)` |
| Card border | `--border-color` (`#404854`) |
| Separator | `rgba(64, 72, 84, 0.3)` |
| Stat label | `--text-secondary` (`#808080`) |
| Stat value | `--accent-gold` (`#d4af37`) |

### Variants

| Variant | Modifier | Effect |
|---------|----------|--------|
| Default | (none) | Standard character card |
| Compact | (via dev override `padding: 12px 15px`) | For mobile < 768px |

### Behaviour

- **Passive** — no interaction, animation, or hover states
- **Dynamic** — values are populated by JS (`dashboard.js`) data binding
- **Responsive** — font sizes shrink on mobile (< 768px): labels → 12px, values → 14px

### Example

```html
<div class="character-card">
    <div class="stat-row">
        <span class="stat-label">⚔️ Class</span>
        <span class="stat-value" id="player-class">Warrior</span>
    </div>
    <div class="stat-row">
        <span class="stat-label">Level</span>
        <span class="stat-value" id="player-level">12</span>
    </div>
    <div class="stat-row">
        <span class="stat-label">💰 Coins</span>
        <span class="stat-value" id="player-coins">120</span>
    </div>
</div>
```

### Source

**CSS:** `frontend/css/main.css` — `.character-card`, `.stat-row`, `.stat-label`, `.stat-value`  
**JS:** `frontend/js/dashboard.js` — `showDashboard()` populates stat values  
**HTML:** `frontend/index.html` — inside `#dashboard-screen`

---

## 5. GamePanel

### Purpose

Container panel for game screen content — player info, game area, action buttons. Three variants form a 3-column grid layout on desktop.

### HTML Structure

```html
<!-- Within .game-content grid -->
<div class="player-panel">
    <h3 class="panel-title">Character</h3>
    <div class="player-info">
        <p>Name: <span>Sir Galahad</span></p>
        <!-- ... -->
    </div>
</div>

<div class="game-area">
    <p class="coming-soon">⚔️ Adventure awaits...</p>
</div>

<div class="actions-panel">
    <h3 class="panel-title">Actions</h3>
    <button class="btn btn-primary">Quest Log</button>
    <button class="btn btn-secondary">Settings</button>
</div>
```

### CSS Classes

| Class | Purpose |
|-------|---------|
| `.player-panel` | Left column — character stats |
| `.game-area` | Center column — main game content |
| `.actions-panel` | Right column — stacked action buttons |
| `.panel-title` | Title for any panel — gold, uppercase, bottom border |
| `.player-info` | Content wrapper inside `.player-panel` |
| `.coming-soon` | Placeholder text for unimplemented game area |

### Dimensions

| Property | Value |
|----------|-------|
| Padding | `15px` |
| Border | `2px solid var(--accent-gold)` (`#d4af37`) |
| Border radius | `4px` |
| Background | `var(--tertiary-dark)` (`#1a1a2e`) |
| Box shadow | `var(--shadow)` + gold glow on game screen |

### Colors

| Element | Color |
|---------|-------|
| Background | `--tertiary-dark` (`#1a1a2e`) |
| Border | `--accent-gold` (`#d4af37`) |
| Panel title | `--accent-gold` (`#d4af37`) |
| Title separator | `--border-color` (`#404854`) |
| Player info text | `--text-primary` (`#c0c0c0`) |
| Player info value highlights | `--accent-gold` (`#d4af37`) |
| Coming soon | `--text-secondary` (`#808080`) |

### Glow (Game Screen Only)

When inside `.game-screen`, panels receive an additional glow shadow:

```css
box-shadow:
    0 0 10px rgba(212, 175, 55, 0.3),
    0 0 20px rgba(233, 69, 96, 0.2),
    inset 0 0 10px rgba(212, 175, 55, 0.1);
```

### Grid Layout

**Desktop (> 768px):**
```css
.game-content {
    display: grid;
    grid-template-columns: 250px 1fr 150px;
    gap: 20px;
    max-width: 1000px;
}
```

**Mobile (≤ 768px):**
```css
.game-content {
    grid-template-columns: 1fr;
}
```

### Behaviour

- **Passive containers** — no interaction states
- **Responsive** — single column stack on mobile
- **Actions panel** — buttons stack vertically with `gap: 10px`; max 6 buttons

### Example

```html
<div class="game-screen">
    <div class="game-header">
        <h1 class="game-title">LIFE QUEST</h1>
    </div>
    <div class="game-content">
        <div class="player-panel">
            <h3 class="panel-title">Character</h3>
            <div class="player-info">
                <p>Name: <span id="g-name">—</span></p>
                <p>HP: <span id="g-hp">—</span></p>
            </div>
        </div>
        <div class="game-area">
            <p class="coming-soon">⚔️ Adventure awaits...</p>
        </div>
        <div class="actions-panel">
            <h3 class="panel-title">Actions</h3>
            <button class="btn btn-primary">Quest Log</button>
            <button class="btn btn-secondary">Logout</button>
        </div>
    </div>
</div>
```

### Source

**CSS:** `frontend/css/main.css` — `.game-screen`, `.game-header`, `.game-content`, `.player-panel`, `.game-area`, `.actions-panel`, `.panel-title`, `.player-info`, `.coming-soon`  
**CSS:** `frontend/css/dark-fantasy.css` — glow overrides for `.game-screen .player-panel`, `.game-screen .game-area`, `.game-screen .actions-panel`  
**HTML:** (future game screen)

---

## 6. WoodSign

### Purpose

A decorative wooden signboard with chains and nails, used for auth screens, dashboard, error screens, settings — any content that needs a "medieval tavern notice" feel.

### HTML Structure

```html
<div class="sign-hanger">
    <div class="sign-hook"></div>
    <div class="sign-chains">
        <div class="sign-chain sign-chain-left"></div>
        <div class="sign-chain sign-chain-right"></div>
    </div>
    <div class="wood-sign">
        <div class="wood-sign-plank-lines"></div>
        <!-- Content goes here -->
        <h1 class="game-title">LIFE QUEST</h1>
    </div>
</div>
```

### Component Hierarchy

```
.sign-hanger (flex column, centered, sways)
├── .sign-hook (top hook, absolute positioned)
├── .sign-chains (flex row, spacers for left/right chains)
│   ├── .sign-chain.sign-chain-left (rotated -3°)
│   └── .sign-chain.sign-chain-right (rotated +3°)
└── .wood-sign (main board)
    └── .wood-sign-plank-lines (decorative overlay, pointer-events: none)
```

### CSS Classes

| Class | Purpose |
|-------|---------|
| `.sign-hanger` | Outer container — centers the sign, applies sway animation |
| `.sign-hook` | Top hook — arch shape (`border-radius: 10px 10px 0 0`) |
| `.sign-chains` | Chain row container — 52px height, flex with space-between |
| `.sign-chain` | Single chain link — repeating-linear-gradient for chain texture |
| `.sign-chain-left` | Left chain — `rotate(-3deg)` |
| `.sign-chain-right` | Right chain — `rotate(3deg)` |
| `.wood-sign` | Main board — wood gradient, 6px border, 3D shadow, nails |
| `.wood-sign::before` | Left nail — 8px circle, radial gradient |
| `.wood-sign::after` | Right nail — 8px circle, radial gradient |
| `.wood-sign-plank-lines` | Vertical plank separator overlay |

### Dimensions

| Part | Property | Value |
|------|----------|-------|
| Sign width | `width` | `min(420px, 88vw)` |
| Sign padding | `padding` | `28px 24px 24px` |
| Sign border | `border` | `6px solid var(--wood-edge)` |
| Sign border radius | `border-radius` | `2px` |
| Chain height | `height` | `52px` |
| Chain width | `width` | `10px` |
| Chain padding gap | `padding: 0 24px` | Spacing between chains |
| Nail size | `width/height` | `8px` |
| Hook width | `width` | `20px` |
| Hook height | `height` | `12px` |
| Hook border | `border` | `4px solid var(--chain-metal)` |

### Colors

| Part | Color |
|------|-------|
| Sign background | `linear-gradient(180deg, #c8956c, #a06840, #6b4423)` |
| Sign border | `--wood-edge` (`#4a2e18`) |
| Chain metal | `--chain-metal` (`#8a8a9a`) |
| Chain shadow | `--chain-shadow` (`#4a4a58`) |
| Nail bright | `#888` |
| Nail shadow | `#555` |
| Plank line | `rgba(0,0,0,0.06)` |
| Hook | `--chain-metal` (`#8a8a8a`) |

### Shadows

```css
.wood-sign {
    box-shadow:
        inset 0 2px 0 rgba(255,255,255,0.15),   /* top highlight */
        inset 0 -4px 0 rgba(0,0,0,0.2),          /* bottom shadow */
        0 8px 0 var(--wood-edge),                 /* 3D bottom edge */
        0 12px 24px rgba(0,0,0,0.45);             /* drop shadow */
}
```

### Animations

| Element | Animation | Duration | Timing |
|---------|-----------|----------|--------|
| `.sign-hanger` | `sign-sway` (rotate -0.6° → 0.6°) | 5s | `ease-in-out infinite` |
| `.sign-chain-left` | Inherits sway (fixed -3° offset) | — | — |
| `.sign-chain-right` | Inherits sway (fixed +3° offset) | — | — |

### Behaviour

- **Passive container** — the wood sign itself has no interaction states
- **Sway animation** must respect `prefers-reduced-motion: reduce` → turn off
- **Responsive:** On ≤ 480px, padding reduces to `20px 16px 18px`, chain height to 40px, windmill scales to 0.75

### Content Scoping

Classes that are **automatically styled** when placed inside `.wood-sign`:

| Class | Effect |
|-------|--------|
| `.game-title` | Pixel font, `--wood-edge` color, no glow, clamp sizing |
| `.game-subtitle` | Pixel font, `#6b4423` color, clamp sizing |
| `.form-title` | Pixel font, `--wood-edge` color, clamp sizing |
| `.form-label` | Pixel font, `--wood-edge` color, clamp sizing |
| `.form-input` | Cream bg, pixel font, wood edge border, 3D shadow |
| `.form-hint` | Pixel font, `rgba(107,68,35,0.7)` color, clamp sizing |
| `.welcome-message` | Pixel font, `#5a3820` color, clamp sizing |
| `.btn` | Pixel font, wood edge border, 3D shadows + gradients |
| `.btn-primary` | Green gradient background |
| `.btn-success` | Gold gradient background |
| `.btn-secondary` | Transparent cream background |
| `.error-message` | Pixel font, red theme, clamp sizing |
| `.success-message` | Pixel font, green theme, clamp sizing |
| `.auth-header` | Dashed `--wood-edge` bottom border |
| `.dashboard-header` | (no override — uses default) |

### Example (Loading Screen)

```html
<div class="sign-hanger">
    <div class="sign-hook"></div>
    <div class="sign-chains">
        <div class="sign-chain sign-chain-left"></div>
        <div class="sign-chain sign-chain-right"></div>
    </div>
    <div class="wood-sign loading-container">
        <div class="wood-sign-plank-lines"></div>
        <h1 class="game-title">LIFE QUEST</h1>
        <p class="loading-text" id="loading-text">Connecting to the realm...</p>
    </div>
</div>
```

### Source

**CSS:** `frontend/css/pixel-scene.css` — all `.sign-*`, `.wood-sign`, `.wood-sign::before`, `.wood-sign::after`, `.wood-sign-plank-lines`, `.wood-sign .*` scoped rules  
**HTML:** `frontend/index.html` — `#loading-screen`, `#dashboard-screen`, `#error-screen`

---

## 7. Message

### Purpose

Feedback message for success or error states. Appears below forms, panels, or action results.

### HTML Structure

```html
<div class="error-message" id="error-msg" role="alert" aria-live="polite">
    Invalid username or password.
</div>

<div class="success-message" id="success-msg" role="status" aria-live="polite">
    Character created successfully!
</div>
```

### CSS Classes

| Class | Purpose |
|-------|---------|
| `.error-message` | Error feedback — red bg, red border |
| `.success-message` | Success feedback — green bg, green border |
| `.error-message.show` | Visible state (`display: block`) |
| `.success-message.show` | Visible state (`display: block`) |

### Dimensions

| Property | Value |
|----------|-------|
| Padding | `10px` |
| Margin top | `15px` |
| Border radius | `4px` (dark UI) / `0` (wood sign) |
| Border width | `1px` (dark UI) / `2px` (wood sign) |
| Font size | `13px` (dark UI) / clamp (wood sign) |

### Colors

| Context | Error Bg | Error Border | Error Text | Success Bg | Success Border | Success Text |
|---------|----------|-------------|------------|-----------|---------------|-------------|
| Dark UI | `rgba(244, 67, 54, 0.2)` | `--error` (`#f44336`) | `#ff6b6b` | `rgba(76, 175, 80, 0.2)` | `--success` (`#4caf50`) | `#81c784` |
| Wood sign | `rgba(139, 32, 32, 0.15)` | `#8b2020` | `#8b2020` | `rgba(58, 122, 40, 0.15)` | `#3a7a28` | `#3a7a28` |

### Behaviour

- **Hidden by default** (`display: none`) — shown by adding class `.show`
- **Animated** — no animation; instant show/hide
- **Accessibility** — `role="alert"` or `role="status"` + `aria-live="polite"` for screen readers

### Example

```html
<div class="error-message show" id="login-error" role="alert" aria-live="polite">
    ⚠️ Invalid credentials. Please try again.
</div>

<div class="success-message show" id="save-success" role="status" aria-live="polite">
    ✅ Character saved successfully!
</div>
```

### Source

**CSS:** `frontend/css/main.css` — `.error-message`, `.success-message`, `.error-message.show`, `.success-message.show`  
**CSS:** `frontend/css/pixel-scene.css` — `.wood-sign .error-message`, `.wood-sign .success-message`

---

## 8. LoadingOverlay

### Purpose

Displays an animated loading state while the app initialises or performs a background operation.

### HTML Structure

```html
<div class="loading-container">
    <h1 class="game-title">LIFE QUEST</h1>
    <p class="loading-text" id="loading-text">Connecting to the realm...</p>
</div>
```

### CSS Classes

| Class | Purpose |
|-------|---------|
| `.loading-container` | Centered container — `text-align: center`, padding |
| `.loading-text` | Animated text — `pulse-text` animation, `--text-primary` |

### Dimensions

| Property | Value |
|----------|-------|
| Container padding | `30px 20px` |
| Text font size | `16px` |
| Text margin top | `20px` |

### Animation

```css
@keyframes pulse-text {
    0%, 100% { opacity: 0.6; }
    50% { opacity: 1; }
}

.loading-text {
    animation: pulse-text 1.5s ease-in-out infinite;
}
```

### Behaviour

- **Visible** by default on loading screen (#loading-screen)
- **Replaced** by error or dashboard screen once session resolves
- **Dynamic text** — JS updates `#loading-text` content (`updateLoadingText()`)

### Example

```html
<div class="loading-container">
    <h1 class="game-title">LIFE QUEST</h1>
    <p class="loading-text" id="loading-text">Verifying your identity...</p>
</div>
```

### Source

**CSS:** `frontend/css/main.css` — `.loading-container`, `.loading-text`, `@keyframes pulse-text`  
**JS:** `frontend/js/dashboard.js` — `updateLoadingText()`, `showNotRegistered()`, `showDashboard()`  
**HTML:** `frontend/index.html` — `#loading-screen`

---

## 9. Screen

### Purpose

Base wrapper for every application screen. Provides absolute positioning, full viewport coverage, and activation via `.active` class.

### HTML Structure

```html
<div id="screen-name" class="screen screen-name">
    <!-- Screen content -->
</div>
```

### CSS Classes

| Class | Purpose |
|-------|---------|
| `.screen` | Base — `display: none`, `position: absolute`, full viewport |
| `.screen.active` | Visible — `display: flex`, centered content |
| `.screen.screen-name` | Per-screen styles — background, padding, alignment |

### CSS

```css
.screen {
    display: none;
    width: 100%;
    height: 100%;
    position: absolute;
    top: 0;
    left: 0;
}

.screen.active {
    display: flex;
    align-items: center;
    justify-content: center;
}
```

### Screen Types

| Screen ID | Classes | Purpose | Background |
|-----------|---------|---------|------------|
| `#loading-screen` | `.screen.loading-screen` | App initialisation | Full pixel scene |
| `#dashboard-screen` | `.screen.dashboard-screen` | Character stats | Simplified pixel scene |
| `#error-screen` | `.screen.error-screen` | Not registered / error | Simplified pixel scene |
| (future) `#game-screen` | `.screen.game-screen` | Game play | Dark gradient + scanlines |

### Behaviour

- **Only one screen** can have `.active` at a time.
- **Switching:** `hideAllScreens()` removes `.active` from all `.screen`, then add `.active` to target.
- **Responsive:** All screens have `width: 100%; height: 100%` — content scrolls if overflow.

### JS API

```javascript
function hideAllScreens() {
    document.querySelectorAll('.screen').forEach(function (screen) {
        screen.classList.remove('active');
    });
}

function showScreen(id) {
    hideAllScreens();
    document.getElementById(id).classList.add('active');
}
```

### Source

**CSS:** `frontend/css/main.css` — `.screen`, `.screen.active`, `.auth-screen`, `.dashboard-screen`, `.loading-screen`, `.error-screen`  
**JS:** `frontend/js/dashboard.js` — `hideAllScreens()`, `showDashboard()`, `showNotRegistered()`  
**HTML:** `frontend/index.html` — `#loading-screen`, `#dashboard-screen`, `#error-screen`

---

## 10. PixelScene

### Purpose

Full-screen pixel art landscape background. Used on auth-style screens (loading, dashboard, error). Supports simplified (sky + hills only) and full (sky + hills + village + wheat + walkers) variants.

### HTML Structure (Full)

```html
<div class="pixel-scene" aria-hidden="true">
    <div class="pixel-sky"></div>
    <div class="pixel-sun"></div>
    <div class="pixel-cloud pixel-cloud-1"></div>
    <div class="pixel-cloud pixel-cloud-2"></div>
    <div class="pixel-hills">
        <div class="pixel-hill pixel-hill-far"></div>
        <div class="pixel-hill pixel-hill-near"></div>
    </div>
    <div class="pixel-village">
        <div class="pixel-house pixel-house-left">
            <div class="house-roof"></div>
            <div class="house-body">
                <div class="house-window"></div>
                <div class="house-door"></div>
            </div>
        </div>
        <div class="pixel-windmill">
            <div class="windmill-blades"></div>
            <div class="windmill-tower"></div>
        </div>
        <div class="pixel-house pixel-house-right">
            <div class="house-roof"></div>
            <div class="house-body">
                <div class="house-window"></div>
                <div class="house-door"></div>
            </div>
        </div>
    </div>
    <div class="pixel-wheat-field">
        <div class="wheat-row"></div>
        <div class="wheat-stalks"></div>
        <div class="wheat-stalks wheat-stalks-2"></div>
        <div class="path-edge path-edge-left"></div>
        <div class="path-edge path-edge-right"></div>
    </div>
    <div class="pixel-path"></div>
    <div class="pixel-walkers">
        <div class="pixel-walker walker-1"></div>
        <div class="pixel-walker walker-2"></div>
        <div class="pixel-walker walker-3"></div>
    </div>
</div>
```

### HTML Structure (Simplified — Dashboard, Error)

```html
<div class="pixel-scene" aria-hidden="true">
    <div class="pixel-sky"></div>
    <div class="pixel-sun"></div>
    <div class="pixel-cloud pixel-cloud-1"></div>
    <div class="pixel-cloud pixel-cloud-2"></div>
    <div class="pixel-hills">
        <div class="pixel-hill pixel-hill-far"></div>
        <div class="pixel-hill pixel-hill-near"></div>
    </div>
</div>
```

### Component Inventory

| Element | Class(es) | Z-Index | Description |
|---------|-----------|---------|-------------|
| Scene wrapper | `.pixel-scene` | `0` | Absolute fill, `pointer-events: none` |
| Sky gradient | `.pixel-sky` | — | 5-stop vertical gradient (purple → orange → gold) |
| Sun | `.pixel-sun` | — | 64×64px circle, multi-layer glow, pulsing animation |
| Cloud 1 | `.pixel-cloud.pixel-cloud-1` | — | 80×24px, box-shadow pixels, right drift |
| Cloud 2 | `.pixel-cloud.pixel-cloud-2` | — | 60×20px, box-shadow pixels, left drift |
| Hills container | `.pixel-hills` | — | Absolute, bottom 28%, 120px height |
| Far hill | `.pixel-hill.pixel-hill-far` | — | Purple, `clip-path` polygon |
| Near hill | `.pixel-hill.pixel-hill-near` | — | Green, `clip-path` polygon |
| Village container | `.pixel-village` | — | Absolute, bottom 30%, 140px height |
| Windmill | `.pixel-windmill` | — | 80×120px, tower + spinning blades |
| Left house | `.pixel-house.pixel-house-left` | — | 56×56px, roof + body + window + door |
| Right house | `.pixel-house.pixel-house-right` | — | 48×48px, roof + body + window + door |
| Wheat field | `.pixel-wheat-field` | — | Bottom 32%, gradient + stalk pattern |
| Wheat row | `.wheat-row` | — | Vertical stripe pattern, 0.4 opacity |
| Wheat stalks | `.wheat-stalks` | — | SVG background tile, sway animation |
| Path edge left | `.path-edge.path-edge-left` | — | Trampled wheat, diagonal gradient |
| Path edge right | `.path-edge.path-edge-right` | — | Trampled wheat, diagonal gradient |
| Dirt path | `.pixel-path` | — | 80px wide, trapezoid clip, horizontal line pattern |
| Walkers container | `.pixel-walkers` | — | z-index 1, full inset |
| Walker 1 | `.pixel-walker.walker-1` | — | 8×12px, box-shadow sprite, walks right, 18s |
| Walker 2 | `.pixel-walker.walker-2` | — | 8×12px, box-shadow sprite, walks right, 24s |
| Walker 3 | `.pixel-walker.walker-3` | — | 8×12px, box-shadow sprite, walks left, 22s |

### Variants

| Variant | HTML Elements | Used On |
|---------|--------------|---------|
| **Full scene** | Sky + sun + clouds + hills + village + wheat + path + walkers | `#loading-screen` |
| **Simplified** | Sky + sun + clouds + hills (no village, wheat, walkers) | `#dashboard-screen`, `#error-screen` |
| **Minimal** | (future) Sky + sun + hills | Future screens |

### Animations

| Element | Animation | Duration | GPU Accelerated |
|---------|-----------|----------|-----------------|
| `.pixel-sun` | `sun-pulse` (scale 1→1.05, opacity 1→0.92) | 6s | Yes (transform, opacity) |
| `.pixel-cloud-1` | `cloud-drift` (translateX 0→60px) | 40s linear | Yes (transform) |
| `.pixel-cloud-2` | `cloud-drift` (translateX 0→60px, reverse) | 55s linear | Yes (transform) |
| `.windmill-blades` | `blades-spin` (rotate 0→360deg) | 8s linear | Yes (transform) |
| `.house-window` | `window-glow` (opacity 1→0.7) | 3s | Yes (opacity) |
| `.wheat-stalks` | `wheat-sway` (skewX 0→1.5deg) | 4-5s | Yes (transform) |
| `.walker-1` | `walk-right` (left -3%→103%) + `walker-bob` (translateY) | 18s + 0.4s | Yes (transform) |
| `.walker-2` | `walk-right` + `walker-bob` | 24s + 0.45s | Yes (transform) |
| `.walker-3` | `walk-left` + `walker-bob` | 22s + 0.42s | Yes (transform) |

All animations **must stop** when `prefers-reduced-motion: reduce` is active.

### Accessibility

- **Entire scene** has `aria-hidden="true"` — it's purely decorative.
- **No text or interactive elements** inside `.pixel-scene`.

### Source

**CSS:** `frontend/css/pixel-scene.css` — all `.pixel-*`, `.windmill-*`, `.house-*`, `.wheat-*`, `.path-*`, `.walker-*`, `.sign-*` classes  
**HTML:** `frontend/index.html` — full scene in `#loading-screen`, simplified in `#dashboard-screen` and `#error-screen`

---

## 11. Modal

### Purpose

Overlay dialog for confirmations (e.g. delete account). Darkens the background and presents a focused action panel.

### HTML Structure

```html
<div id="modal-id" class="modal-overlay hidden">
    <div class="modal-content" role="dialog" aria-modal="true" aria-labelledby="modal-title">
        <h2 id="modal-title" class="modal-title">Confirm Action</h2>
        <p class="modal-body">Are you sure?</p>
        <div class="modal-actions">
            <button class="btn btn-secondary" id="cancel-btn">Cancel</button>
            <button class="btn btn-primary" id="confirm-btn">Confirm</button>
        </div>
    </div>
</div>
```

### CSS Classes

(Currently uses `#delete-modal` with inline classes — future refactoring target.)

| Class | Purpose |
|-------|---------|
| `.modal-overlay` | Full-screen dark overlay, `z-index: 50` |
| `.modal-content` | Centered content panel |
| `.modal-title` | Modal heading |
| `.modal-body` | Modal description |
| `.modal-actions` | Button row — flex, gap |

### Behaviour

- **Shown:** Remove `.hidden` class
- **Hidden:** Add `.hidden` class
- **Escape key:** Should close modal
- **Overlay click:** Should close modal (future enhancement)
- **Focus trap:** First focusable element gets focus on open

### Current Implementation (ui.js)

```javascript
// Show modal
els.deleteModal.classList.remove('hidden');
els.deletePassword.value = '';
els.deletePassword.focus();

// Hide modal
els.deleteModal.classList.add('hidden');
```

### Source

**JS:** `frontend/js/ui.js` — `#delete-modal`, `showView()`, event listeners  
**HTML:** (not yet in `index.html` — defined in ui.js references; to be added in future game screen)

---

## 12. Avatar

### Purpose

Displays the player character's avatar as an emoji (current) or pixel-art PNG (future).

### HTML Structure (Current)

```html
<span class="stat-value" id="player-avatar">⚔️</span>
```

### Future Structure

```html
<img
    class="avatar"
    src="asset/characters/knight-32x32.png"
    alt="Knight class avatar"
    width="32"
    height="32"
    loading="lazy"
/>
```

### CSS Classes (Future)

| Class | Purpose |
|-------|---------|
| `.avatar` | Avatar image — `width: 32px` or `48px`, `height: auto`, `image-rendering: pixelated` |
| `.avatar--sm` | Small (32×32) |
| `.avatar--md` | Medium (48×48) |

### Behaviour

- **Emoji fallback** — until PNG sprites are integrated, use class emojis: `⚔️` Adventurer/Warrior, `🔮` Mage, `🏹` Ranger, `🛡️` Knight
- **Transparent PNG** — sprites from `asset/creting_cha_texture/character/`
- **Crisp rendering** — `image-rendering: pixelated`

### Source

**CSS:** (future — not yet implemented)  
**JS:** `frontend/js/ui.js` — `renderProfile()`, class emoji mapping  
**Assets:** `asset/creting_cha_texture/character/`

---

## 13. ProgressBar

### Purpose

Visual indicator for numeric values like HP, XP, or progress. Not yet implemented — this is a placeholder specification for future implementation.

### HTML Structure (Proposed)

```html
<div class="progress-bar" role="progressbar" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100">
    <div class="progress-bar__fill" style="width: 75%"></div>
    <span class="progress-bar__label">75 / 100</span>
</div>
```

### CSS Classes (Proposed)

| Class | Purpose |
|-------|---------|
| `.progress-bar` | Outer container — dark bg, 4px border-radius, 8px height |
| `.progress-bar__fill` | Filled portion — gradient from `--accent-red` to `--accent-gold` |
| `.progress-bar__label` | Optional label overlay |

### Behaviour (Proposed)

- **Width** set via inline `style` or CSS custom property `--progress`
- **Animation:** Smooth width transition (`transition: width 0.5s ease`)
- **Colors:** 
  - HP bar: Red (`--accent-red`) gradient
  - XP bar: Gold (`--accent-gold`) gradient
- **Accessibility:** `role="progressbar"` with `aria-valuenow`, `aria-valuemin`, `aria-valuemax`

### Source

Not yet implemented — see `ui_style.md` section for visual reference.

---

## 14. Quick Reference

### Component Mapping

| Component | CSS File | JS File | HTML Location |
|-----------|----------|---------|---------------|
| **Button** | `main.css`, `pixel-scene.css` | `dashboard.js` | All screens |
| **FormInput** | `main.css`, `pixel-scene.css` | — | Auth screens (future) |
| **CharacterCard** | `main.css` | `dashboard.js` | `#dashboard-screen` |
| **GamePanel** | `main.css`, `dark-fantasy.css` | — | `#game-screen` (future) |
| **WoodSign** | `pixel-scene.css` | — | `#loading-screen`, `#dashboard-screen`, `#error-screen` |
| **Message** | `main.css`, `pixel-scene.css` | — | Auth forms (future) |
| **LoadingOverlay** | `main.css` | `dashboard.js` | `#loading-screen` |
| **Screen** | `main.css` | `dashboard.js` | All screens |
| **PixelScene** | `pixel-scene.css` | — | `#loading-screen`, `#dashboard-screen`, `#error-screen` |
| **Modal** | (future) | `ui.js` | (future) |
| **Avatar** | (future) | `ui.js`, `dashboard.js` | `#dashboard-screen` |
| **ProgressBar** | (future) | — | (future) |

### CSS Custom Properties

All components rely on these `:root` variables (defined in `main.css` and `pixel-scene.css`):

```css
/* Dark UI (main.css) */
--primary-dark: #0a0e27;
--secondary-dark: #16213e;
--tertiary-dark: #1a1a2e;
--accent-red: #e94560;
--accent-gold: #d4af37;
--text-primary: #c0c0c0;
--text-secondary: #808080;
--success: #4caf50;
--error: #f44336;
--border-color: #404854;
--shadow: 0 0 10px rgba(0, 0, 0, 0.8);

/* Pixel Scene (pixel-scene.css) */
--wood-edge: #4a2e18;
--wood-mid: #a06840;
--chain-metal: #8a8a9a;
--wheat-mid: #c9a030;
--wheat-light: #e8c547;
/* ... (see design_tokens.json for full list) */

/* Fonts (pixel-fonts.css) */
--font-pixel: 'Courier New', 'Consolas', 'Monaco', monospace;
--font-mono: 'Courier New', 'Consolas', monospace;
--font-ui: 'Arial', sans-serif;
```

### Checklist for Adding a New Component

- [ ] Does an existing component already cover this use case? Extend it instead.
- [ ] Is the component reusable across at least 2 different screens?
- [ ] Does it follow BEM-lite naming (kebab-case, `__` elements, `--` modifiers)?
- [ ] Are dimensions multiples of 2px (pixel-perfect)?
- [ ] Is there a `prefers-reduced-motion: reduce` fallback for animations?
- [ ] Is the component tested at 320px minimum width?
- [ ] Are color values referenced from CSS custom properties (not hardcoded hex)?
- [ ] Does interactive content meet 44×44px touch target minimum?
- [ ] Is `aria-label` / `role` / `aria-live` applied for accessibility?
- [ ] Has this file (`components.md`) been updated with the new component?

---

> **End of Component Library.**  
> AI agents: Before writing any new UI code, check:
> 1. `design_tokens.json` for exact values
> 2. `ui_style.md` for visual rules
> 3. `components.md` (this file) for reusable components
>
> If a component needs modification, update all three files.
