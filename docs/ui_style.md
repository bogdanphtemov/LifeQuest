# LifeQuest — UI Style Guide

> **Disclaimer for AI agents:** This document defines the canonical visual language of LifeQuest.  
> Every new screen, component, or menu MUST follow these rules to maintain stylistic unity.  
> Before writing any CSS or HTML, re-read the relevant section of this guide.

---

## AI Priority

If this document conflicts with another design-related document, use the following priority chain:

**Highest priority**  →  `docs/design_tokens.json`  *(precise values — colors, spacing, sizes, shadows)*  
**Medium priority**   →  `docs/ui_style.md`  *(this document — visual language, style decisions)*  
**Lowest priority**   →  `docs/components.md`  *(component implementation details, code patterns)*

> **Rule:** `design_tokens.json` always wins for raw values. `ui_style.md` wins for visual decisions.  
> `components.md` only contains implementation — never contradict the style guide.

---

## Table of Contents

1. [AI Priority & Document Hierarchy](#1-ai-priority)
2. [Art Style & Atmosphere](#2-art-style--atmosphere)
3. [Color Palette](#3-color-palette)
4. [Typography](#4-typography)
5. [Buttons — When to Use](#5-buttons--when-to-use)
6. [Cards & Panels](#6-cards--panels)
7. [Glow & Lighting](#7-glow--lighting)
8. [Gradients](#8-gradients)
9. [Component References](#9-component-references)
10. [New Screen Construction Rules](#10-new-screen-construction-rules)
11. [Menu Construction Rules](#11-menu-construction-rules)
12. [Icon Usage Rules](#12-icon-usage-rules)
13. [Character Usage Rules](#13-character-usage-rules)
14. [Animation & Motion](#14-animation--motion)
15. [Layout & Spacing System](#15-layout--spacing-system)
16. [Texture & Material Library](#16-texture--material-library)
17. [Image & Illustration Rules](#17-image--illustration-rules)
18. [CSS Naming Convention](#18-css-naming-convention)
19. [Accessibility](#19-accessibility)
20. [Forbidden UI](#20-forbidden-ui)
21. [Quick Reference Card](#21-quick-reference-card)

---

## 2. Art Style & Atmosphere

### 2.1 Core Aesthetic

**Primary style:** Dark Fantasy Pixel Art (16-bit era inspired).  
**Secondary influence:** Soul Knight (character sprites, dungeon backgrounds).  
**Mood:** Mystical, adventurous, medieval fantasy with a dark undertone.

The interface combines two visual registers:

| Register | Where Used | Description |
|----------|-----------|-------------|
| **Full pixel scene** | Auth screens, loading screen | Hand-crafted CSS pixel art with animated elements (sky, clouds, windmill, wheat field, walkers) |
| **Dark fantasy UI** | Dashboard, game screens, panels | Dark backgrounds with gold/red accents, glowing borders, CRT scanlines |

### 2.2 Visual Atmosphere Keywords

```
mystical       adventurous     medieval
dark           fantasy         pixelated
retro-gaming   urns / torches  stone & wood
golden glow    red accents     starry / twilight sky
```

### 2.3 References (from `asset/creting_cha_texture/`)

**Character inspirations (Soul Knight style):**

- Pixel-art RPG characters, ~32–64px tall
- Crisp edges, limited color palettes (4–8 colors per character)
- Classes visible at a glance: Knight (armor/blue), Rogue (dark/hooded), Mage (robe/purple), Priest (white/gold)
- Characters have distinctive silhouettes (helmets, capes, weapons)

**Background inspirations (dungeon & fantasy scenes):**

| Image | Style Elements |
|-------|---------------|
| `pixel-art-dungeon-scene-glowing-archway-...webp` | Glowing magical portals, stone arches, blue/purple magical light |
| `fond-de-donjon-d-art-pixel-bits-...webp` | Pixel-art dungeon corridor, stone bricks, torch lighting |
| `dark-mysterious-stone-doorway-lit-by-flickering-torches-...avif` | Gothic stone entrance, skull motifs, warm torch glow |
| `hammerwatch-castle-dungeon-...jpg` | Hammerwatch-style pixel dungeon (green/grey stone) |
| `3e715069c332dc0c61d95cf645b89f77.gif` | Animated pixel scene (torch flicker, ambient particles) |
| `2327eb6b-d3ae-4dd1-9b20-ae7c1f0b8ddb.jpg` | Dark fantasy landscape, purple/blue twilight sky |

---

## 3. Color Palette

### 3.1 Brand Colors (Dark UI)

| Token | Hex | Usage |
|-------|-----|-------|
| `--primary-dark` | `#0a0e27` | Main app background (very dark navy) |
| `--secondary-dark` | `#16213e` | Surface color (forms, inputs, panels) |
| `--tertiary-dark` | `#1a1a2e` | Card / panel background |
| `--accent-red` | `#e94560` | Primary accent — CTAs, emphasis, borders |
| `--accent-gold` | `#d4af37` | Secondary accent — headings, levels, coins |
| `--text-primary` | `#c0c0c0` | Body text on dark backgrounds |
| `--text-secondary` | `#808080` | Muted text, hints, secondary info |
| `--border-color` | `#404854` | Default border, dividers |
| `--success` | `#4caf50` | Success states |
| `--error` | `#f44336` | Error states |

### 3.2 Pixel Scene Colors

| Token | Hex | Usage |
|-------|-----|-------|
| `--sky-top` | `#5b3a8c` | Sky top (deep purple twilight) |
| `--sky-mid` | `#c45a28` | Sky middle (sunset orange) |
| `--sky-low` | `#f0a830` | Sky low (golden horizon) |
| `--sky-glow` | `#ffe566` | Sun & glow |
| `--hill-far` | `#3d2860` | Distant hills (purple shadow) |
| `--hill-near` | `#2d6b35` | Near hills (dark green) |
| `--wheat-light` | `#e8c547` | Wheat highlights |
| `--wheat-mid` | `#c9a030` | Wheat mid-tones |
| `--wheat-dark` | `#8b6914` | Wheat shadows |
| `--path-color` | `#c4a060` | Dirt path main |
| `--path-dark` | `#8b7040` | Dirt path shadow |
| `--wood-light` | `#c8956c` | Wood (light) |
| `--wood-mid` | `#a06840` | Wood (mid) |
| `--wood-dark` | `#6b4423` | Wood (dark) |
| `--wood-edge` | `#4a2e18` | Wood edge/border |
| `--chain-metal` | `#8a8a9a` | Chain metal link |
| `--chain-shadow` | `#4a4a58` | Chain shadow |
| `--roof-red` | `#8b3030` | House roof |
| `--roof-dark` | `#5c2020` | Roof shadow |
| `--wall-cream` | `#d4b896` | House wall |
| `--wall-shadow` | `#a08060` | Wall shadow |
| `--mill-white` | `#e8e0d0` | Windmill tower |
| `--mill-blade` | `#6b5030` | Windmill blade |

### 3.3 Color Usage Rules

1. **Dark backgrounds** (`--primary-dark`, `--secondary-dark`, `--tertiary-dark`) are the foundation of all UI.
2. **Gold** (`--accent-gold`) is for: headings, level numbers, coin values, XP values, panel borders.
3. **Red** (`--accent-red`) is for: section dividers, primary CTAs, emphasis, danger indicators.
4. **Never use pure white** (`#ffffff`) — always use off-white/silver (`--text-primary: #c0c0c0`).
5. **Never use pure black** — the darkest color is `--primary-dark: #0a0e27`.
6. **Pixel scene colors** are used exclusively within pixel-art backgrounds — never for UI chrome.
7. **Semantic colors** (success/error) must always be used on a semi-transparent dark background (e.g. `rgba(76, 175, 80, 0.2)`).

---

## 4. Typography

### 4.1 Font Stack

| Role | Stack | Usage |
|------|-------|-------|
| **Pixel font** | `'Press Start 2P', 'Courier New', 'Consolas', 'Monaco', monospace` | Game titles, stat values, buttons, labels on wood signs |
| **Monospace** | `'Courier New', 'Consolas', 'Monaco', monospace` | Input fields, code, data values |
| **UI font** | `'Arial', sans-serif` | Body text, descriptions, notes |

### 4.2 Font Sizing System

**Standard sizes (outside wood sign):**

| Token | Size | Where Used |
|-------|------|-----------|
| `--font-size-xs` | `7px` | Form hints (pixel) |
| `--font-size-sm` | `9px` | Form labels (pixel) |
| `--font-size-md` | `10px` | Buttons, inputs (pixel) |
| `--font-size-base` | `12px` | Error messages, secondary text |
| `--font-size-lg` | `14px` | Form labels, inputs, buttons, stat labels |
| `--font-size-xl` | `15px` | Error content |
| `--font-size-2xl` | `16px` | Stat values, loading text |
| `--font-size-3xl` | `18px` | "Coming soon" text |
| `--font-size-4xl` | `20px` | Form titles |
| `--font-size-5xl` | `24px` | Game title (mobile) |
| `--font-size-6xl` | `28px` | Error game title |
| `--font-size-7xl` | `32px` | Game title (desktop) |

**Clamped sizes (on wood sign — responsive):**

| Token | Clamp | Where Used |
|-------|-------|-----------|
| `--pixel-title` | `clamp(14px, 3.5vw, 20px)` | Game title on wood signs |
| `--pixel-subtitle` | `clamp(8px, 2vw, 10px)` | Subtitle |
| `--pixel-form-title` | `clamp(9px, 2.2vw, 12px)` | Form title |
| `--pixel-label` | `clamp(7px, 1.8vw, 9px)` | Form label |
| `--pixel-input` | `clamp(8px, 2vw, 10px)` | Input text |
| `--pixel-btn` | `clamp(8px, 2vw, 10px)` | Button text |
| `--pixel-hint` | `clamp(6px, 1.5vw, 7px)` | Hint text |
| `--pixel-msg` | `clamp(6px, 1.5vw, 8px)` | Error/success messages |
| `--pixel-welcome` | `clamp(7px, 1.8vw, 9px)` | Welcome paragraph |

### 4.3 Typography Rules

1. **Titles on dark UI:** Use `--accent-gold` color, `letter-spacing: 2px`, `text-shadow` with 2px black offset + gold/red glow.
2. **Titles on wood sign:** Use `--wood-edge` (`#4a2e18`) color, `text-shadow: 2px 2px 0 rgba(0,0,0,0.15)`, NO glow animation.
3. **Stat labels:** Uppercase, `--text-secondary`, `letter-spacing: 1px`, `font-size: 14px`.
4. **Stat values:** `--accent-gold`, bold, monospace font, `font-size: 16px`.
5. **Body text:** `--text-primary`, `Arial`, `line-height: 1.6`.
6. **Pixel font (`Press Start 2P`)** is used ONLY for titles, labels, and buttons — never for long paragraphs.
7. **Never use more than one font size** in a single line of text.

---

## 5. Buttons — When to Use

> **Implementation detail:** All button CSS properties (colors, gradients, shadows, hover states, padding) are defined in `docs/components.md`.  
> This section only tells you **when** to use each variant.

### 5.1 Dark UI Buttons (`.game-screen`, `.dashboard-screen`)

| Variant | Class | When to Use |
|---------|-------|------------|
| **Primary** | `btn btn-primary` | Main actions, danger/delete, emphasis CTAs |
| **Success** | `btn btn-success` | Confirm, save, positive actions |
| **Secondary** | `btn btn-secondary` | Cancel, back, secondary options, dismiss |

### 5.2 Wood Sign Buttons (`.wood-sign`)

| Variant | Class | When to Use |
|---------|-------|------------|
| **Primary** | `btn btn-primary` (green gradient) | Main action on wood sign — "New Game", "Submit" |
| **Success** | `btn btn-success` (gold gradient) | Secondary confirm — "Continue", "Save" |
| **Secondary** | `btn btn-secondary` (transparent) | Tertiary — "Back", "Cancel", "Settings" |

---

## 6. Cards & Panels

### 6.1 Character Card / Stat Card (Dashboard)

```
┌───────────────────────────────┐
│  Name          Sir Galahad    │  ← stat-row
│  Login         knight42       │  ← stat-row
│  Class         Warrior        │  ← stat-row
│  Level         12             │  ← stat-row  (gold value)
│  Experience    3450           │  ← stat-row  (gold value)
│  Coins         120            │  ← stat-row  (gold value)
└───────────────────────────────┘
```

**Properties:**
- `background: rgba(22, 33, 62, 0.5)` (semi-transparent secondary-dark)
- `border: 1px solid var(--border-color)` (`#404854`)
- `border-radius: 4px`
- `padding: 15px 20px`
- **Rows:** `display: flex; justify-content: space-between`, bottom border `rgba(64, 72, 84, 0.3)`
- **Last row:** no border

### 6.2 Game Panels (`.player-panel`, `.game-area`, `.actions-panel`)

**Properties:**
- `background: var(--tertiary-dark)` (`#1a1a2e`)
- `border: 2px solid var(--accent-gold)` (`#d4af37`)
- `border-radius: 4px`
- `padding: 15px`
- `box-shadow: var(--shadow)` (`0 0 10px rgba(0,0,0,0.8)`)
- **On game screen:** additional glow shadow (`0 0 10px rgba(212,175,55,0.3), 0 0 20px rgba(233,69,96,0.2), inset 0 0 10px rgba(212,175,55,0.1)`)
- **Panel title:** `--accent-gold`, 14px, uppercase, bottom border `--border-color`

### 6.3 Wood Sign (`.wood-sign`)

```
        ╤══════════╤          ← chains
        │          │
    ┌───┴──────────┴───┐      ← wood-edge border (6px)
    │  ╔══╗            │      ← nail (8px circle)
    │  ╚══╝            │
    │   LIFE QUEST     │      ← content
    │   ──────────     │      ← plank line
    │                  │
    └──────────────────┘
```

**Construction:**
1. Outer container: `.sign-hanger` (centered, `flex-direction: column`)
2. `.sign-hook` — top hook (20×12px, `border: 4px solid --chain-metal`, `border-radius: 10px 10px 0 0`)
3. `.sign-chains` — two chains (`.sign-chain-left` rotated -3°, `.sign-chain-right` rotated +3°)
   - Width: 10px, Height: 52px
   - `repeating-linear-gradient` for chain link effect
4. `.wood-sign` — main board
   - Width: `min(420px, 88vw)`
   - Background: `linear-gradient(180deg, --wood-light → --wood-mid → --wood-dark)`
   - Border: `6px solid --wood-edge`
   - `border-radius: 2px`
   - Padding: `28px 24px 24px`
   - `box-shadow`: inset highlights + 3D bottom shadow
   - `image-rendering: pixelated`
5. `.wood-sign::before/after` — nail circles (8×8px, radial gradient)
6. `.wood-sign-plank-lines` — vertical plank separators

### 6.4 Card Construction Rules

1. **Cards always have a dark background** (never white or light).
2. **Borders are always 1–2px** — never 0 unless it's a pixel scene element.
3. **Border radius is always small** (0–4px) to maintain pixel-art feel. Never use `border-radius: 8px` or larger for primary UI elements.
4. **Internal spacing** uses `space-y-3` / `gap: 10-15px` system.
5. **Character cards** in dashboard use semi-transparent background (`rgba(22, 33, 62, 0.5)`) to show the scene behind.
6. **Never use box-shadow on cards** unless it's a wood sign or game panel.
7. **Stat rows** must always have `display: flex` with `justify-content: space-between`.

---

## 7. Glow & Lighting

### 7.1 Glow Types

| Type | CSS | Usage |
|------|-----|-------|
| **Gold border glow** | `0 0 10px rgba(212,175,55,0.3), 0 0 20px rgba(233,69,96,0.2), inset 0 0 10px rgba(212,175,55,0.1)` | Game screen panels |
| **Title glow** | `text-shadow: 2px 2px 4px rgba(0,0,0,0.8), 0 0 10px rgba(212,175,55,0.5), 0 0 20px rgba(233,69,96,0.3)` | Game titles on dark UI |
| **Input focus glow** | `box-shadow: 0 0 10px rgba(212,175,55,0.3)` | Input fields on dark UI |
| **Button hover glow** | `box-shadow: 0 0 15px rgba(233,69,96,0.4)` | Primary button hover |
| **Sun glow** | `box-shadow: 0 0 0 4px #f0c040, 0 0 0 8px rgba(240,192,64,0.5), 0 0 40px 12px rgba(255,220,80,0.4)` | Pixel scene sun |
| **Window glow** | `box-shadow: 0 0 6px 2px rgba(255,220,80,0.6)` | House windows at night |

### 7.2 Glow Animation

**Title glow animation** (only on `.game-screen`):
```css
@keyframes glow {
    0%, 100% {
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8),
                     0 0 10px rgba(212,175,55,0.5),
                     0 0 20px rgba(233,69,96,0.3);
    }
    50% {
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8),
                     0 0 20px rgba(212,175,55,0.8),
                     0 0 30px rgba(233,69,96,0.5);
    }
}
```

### 7.3 Glow Rules

1. **Glow is NEVER used on wood sign elements** — wood signs have a flat, grounded look.
2. **Glow is reserved for:** game titles (on dark UI), input focus, button hover, pixel scene sun/windows.
3. **Gold glow** is for panels and titles. **Red glow** is for danger/CTA buttons.
4. **Glow must always use `rgba()`** with partial opacity — never `opacity` on the element itself.
5. **Maximum 2 glow layers** per element — too many layers look muddy on mobile screens.
6. **Glow animation** must respect `prefers-reduced-motion: reduce`.

---

## 8. Gradients

### 8.1 Approved Gradients

| Name | Definition | Usage |
|------|-----------|-------|
| **Game screen bg** | `linear-gradient(135deg, #0a0e27 0%, #16213e 100%)` | Background of `.game-screen` |
| **Pixel sky** | `linear-gradient(180deg, #5b3a8c 0%, #7a4080 18%, #c45a28 45%, #f0a830 72%, #ffe566 100%)` | Pixel scene sky |
| **Wheat field** | `linear-gradient(180deg, #4a8a30 0%, #2d6b35 15%, #8b6914 100%)` | Wheat field ground |
| **Dirt path** | `linear-gradient(180deg, transparent 0%, #c4a060 20%, #8b7040 100%)` | Path overlay |
| **Wood sign** | `linear-gradient(180deg, #c8956c 0%, #a06840 50%, #6b4423 100%)` | Wood sign board |
| **Btn primary (wood)** | `linear-gradient(180deg, #6a9a40 0%, #4a7a28 100%)` | Primary button on wood sign |
| **Btn success (wood)** | `linear-gradient(180deg, #c89030 0%, #a07020 100%)` | Success button on wood sign |

### 8.2 Gradient Rules

1. **Dark UI gradients** always go from a darker shade to a slightly lighter shade (135° angle).
2. **Pixel scene gradients** always go top-to-bottom (180°).
3. **Button gradients (wood sign)** always go top-to-bottom with a 3D shadow for depth.
4. **Never use radial gradients** for UI elements — they break the pixel-art aesthetic.
5. **Radial gradient is used ONLY** for the vignette overlay: `radial-gradient(ellipse at center 40%, transparent 40%, rgba(0,0,0,0.35) 100%)`.

---

## 9. Component References

> **Use `docs/components.md`** for full component implementation (HTML structure, CSS classes, JS logic).  
> This section only maps visual names → component files.

| Visual Component | Defined In | Notes |
|-----------------|------------|-------|
| **Button** (all variants) | `components.md` → Button | Dark UI + Wood sign styles |
| **Wood Sign** | `components.md` → WoodSign | Chains, board, nails, plank lines |
| **Character Card** | `components.md` → CharacterCard | Dashboard stat layout |
| **Game Panel** | `components.md` → GamePanel | `.player-panel`, `.actions-panel` |
| **Input / Form Field** | `components.md` → FormField | Text inputs, labels, validation |
| **Modal / Dialog** | `components.md` → Modal | Overlay + content panel |
| **Action Menu** | `components.md` → ActionMenu | Stacked button list inside game panel |
| **Avatar** | `components.md` → Avatar | Character sprite display |
| **Progress Bar** | `components.md` → ProgressBar | HP/XP bars |

---

## 10. New Screen Construction Rules

### 10.1 Screen Anatomy Template

Every screen in the app follows this structure:

```html
<div id="[screen-name]-screen" class="screen [screen-name]-screen">
    <!-- OPTIONAL: Pixel scene background (if screen is auth/loading style) -->
    <div class="pixel-scene" aria-hidden="true">
        <div class="pixel-sky"></div>
        <div class="pixel-sun"></div>
        <div class="pixel-cloud pixel-cloud-1"></div>
        <div class="pixel-cloud pixel-cloud-2"></div>
        <div class="pixel-hills">
            <div class="pixel-hill pixel-hill-far"></div>
            <div class="pixel-hill pixel-hill-near"></div>
        </div>
        <!-- windmill, village, wheat field only for full scene -->
    </div>

    <!-- OR: Dark fantasy gradient background (for game/dashboard style) -->
    <!-- Background is inherited from .screen or .game-screen -->

    <div class="sign-hanger">
        <!-- OR: directly a .wood-sign or custom container -->
        <div class="wood-sign [name]-container">
            <div class="wood-sign-plank-lines"></div>

            <!-- Content goes here -->

        </div>
    </div>

    <!-- OR: Plain dark panel (for game-style screens) -->
    <div class="[name]-panel">
        ...
    </div>
</div>
```

### 10.2 Screen Style Selection Guide

| Screen Purpose | Background Style | Container Style |
|---------------|-----------------|-----------------|
| **Welcome / Loading** | Full pixel scene (sky, hills, village, wheat) | Wood sign (`.wood-sign`) |
| **Authentication** (login/register) | Full pixel scene | Wood sign (`.wood-sign`) |
| **Dashboard** (character stats) | Simplified pixel scene (sky, hills only) | Wood sign (`.wood-sign`) |
| **Error / Not registered** | Simplified pixel scene (sky, hills only) | Wood sign (`.wood-sign`) |
| **Game / Play** | Dark gradient (`--primary-dark` → `--secondary-dark`) + scanlines | Dark panels (`.player-panel`, etc.) |
| **Settings / Options** | Simplified pixel scene | Wood sign (`.wood-sign`) |
| **Inventory / Items** | Dark gradient + scanlines | Dark panels (`.player-panel`) |
| **Quest / Mission list** | Dark gradient + scanlines | Dark panels (`.player-panel`) |

### 10.3 Screen Activation Rules

1. Every screen has class `.screen` and is hidden by default (`display: none`).
2. To show a screen, add class `.active` (`display: flex; align-items: center; justify-content: center`).
3. Only ONE screen can have `.active` at a time.
4. Switching screens:
   ```js
   hideAllScreens();  // removes .active from all .screen
   document.getElementById('target-screen').classList.add('active');
   ```
5. All screens must have `position: absolute; top: 0; left: 0; width: 100%; height: 100%`.

### 10.4 Responsive Rules for Screens

1. **Mobile (< 480px):** Reduce scene elements (hide village, reduce windmill scale). Container padding: `20px 15px`.
2. **Tablet (480–768px):** Full scene visible. Normal padding.
3. **Desktop (> 768px):** Max container width 500px for wood signs, 1000px for game content.
4. **Minimum viewport:** 320px. Test all new screens at this width.
5. **Wood sign width:** Always `min(420px, 88vw)`.

### 10.5 Adding a New Screen Checklist

- [ ] Add HTML in `index.html` with unique ID `[name]-screen`
- [ ] Add CSS classes in `main.css` (or relevant CSS file)
- [ ] Ensure `.screen` base class is present
- [ ] Add `display: none` / `.active { display: flex }` rules
- [ ] Choose correct background style (pixel scene or dark gradient)
- [ ] Add screen to `hideAllScreens()` targets
- [ ] Add screen to `querySelectorAll('.screen')` coverage
- [ ] Test at 320px, 480px, 768px, 1200px
- [ ] Test with `prefers-reduced-motion: reduce`

---

## 11. Menu Construction Rules

### 11.1 Menu Types

LifeQuest uses **two types of menus**:

| Type | Where | Style |
|------|-------|-------|
| **Action buttons** | Game screen (`.actions-panel`) | Stacked `btn` elements, full width |
| **Wood sign options** | Auth screens, settings | List of links/buttons inside a wood sign |

### 11.2 Action Panel Menu (`.actions-panel`)

```
┌─────────────────┐
│   PANEL TITLE   │  ← panel-title
├─────────────────┤
│  [  QUEST LOG  ]│  ← btn btn-primary
│  [ INVENTORY  ] │  ← btn btn-primary
│  [ SETTINGS   ] │  ← btn btn-secondary
│  [  LOGOUT    ] │  ← btn btn-secondary
└─────────────────┘
```

**Structure:**
```html
<div class="actions-panel">
    <h3 class="panel-title">Actions</h3>
    <button class="btn btn-primary" onclick="...">Quest Log</button>
    <button class="btn btn-primary" onclick="...">Inventory</button>
    <button class="btn btn-secondary" onclick="...">Logout</button>
</div>
```

**Rules:**
1. Buttons are stacked vertically with `gap: 10px`.
2. Primary actions use `btn-primary` (red). Secondary use `btn-secondary` (grey).
3. Maximum 6 buttons per panel. If more are needed, paginate or group.
4. **No icons** in action buttons.

### 11.3 Wood Sign Menu

```
┌──────────────────────────────┐
│                              │
│        LIFE QUEST            │
│    ────────────────          │
│                              │
│   [1] New Game               │  ← btn btn-primary (green)
│                              │
│   [2] Continue               │  ← btn btn-primary (gold)
│                              │
│   [3] Settings               │  ← btn btn-secondary
│                              │
│   [4] About                  │  ← btn btn-secondary
│                              │
└──────────────────────────────┘
```

**Rules:**
1. All buttons use wood sign button styles (`border: 3px solid --wood-edge`, `border-radius: 0`).
2. Primary options use green gradient (`btn-primary` wood style).
3. Secondary options use gold gradient (`btn-success` wood style) or transparent (`btn-secondary`).
4. Title is centered, uses `--wood-edge` color, `Press Start 2P` font.
5. **No numbered lists in HTML** — use CSS counters if needed.

### 11.4 Menu Depth & Navigation Rules

1. **Maximum menu depth:** 2 levels (main menu → submenu).
2. **Back button:** Show Telegram Back button on all submenus. Hide on top-level.
3. **Never create hamburger menus** — Telegram Mini Apps should use flat navigation.
4. **Never use dropdown menus** — they don't translate well to mobile touch interfaces.
5. **Bottom navigation bars** are forbidden — use the Telegram Main Button instead.

---

## 12. Icon Usage Rules

### 12.1 Current Icon System

LifeQuest uses **CSS-only pixel icons** (no icon font, no SVG sprite). Examples:
- **Nails:** `radial-gradient(circle, #888 30%, #555 70%)` — 8×8px circles
- **Windows:** `background: #ffe880` with `box-shadow` glow — 10×10px blocks
- **Doors:** `background: --wood-dark` — 12×18px rectangles

### 12.2 Icon Rules

1. **No external icon libraries** (Font Awesome, Material Icons, etc.) — they conflict with the pixel art aesthetic.
2. **Prefer CSS pixel icons** (box-shadow art, pseudo-elements) over image files.
3. **If an image icon is needed:** use transparent PNG with crisp pixel edges (`image-rendering: pixelated`).
4. **Icon size:** must be multiples of 8px (8×8, 16×16, 24×24, 32×32).
5. **Icon color:** always use a color from the palette — never use `currentColor` for icons.
6. **Emoji are allowed** for simple indicators (⚔️, ⚡, 🛡️) — use sparingly and only in non-critical UI.
7. **Do not create SVG icons** unless they are pixel-perfect (no anti-aliasing).

### 12.3 When to Use Icons

| Context | Icon Type | Example |
|---------|-----------|---------|
| **Stat labels** | Emoji (optional) | ⚔️ Class, 💰 Coins |
| **Decorative scene elements** | CSS pixel art | Sun, clouds, windmill, houses |
| **Indicators** (health, XP) | CSS box-shadow bars | Colored pixel strips |
| **Buttons** | ❌ No icons | Text only |
| **Navigation** | ❌ No icons | Text only |

---

## 13. Character Usage Rules

### 13.1 Character Art Style

Based on the Soul Knight-inspired sprites in `asset/creting_cha_texture/character/`:

- **Style:** Pixel art, 16-bit era
- **Size:** 32–64px height, proportional width
- **Palette:** 4–8 colors per character
- **Edges:** Crisp (`image-rendering: pixelated`)
- **Background:** Transparent PNG / GIF

### 13.2 Character Classes & Visual Identity

| Class | Visual Cues (from sprites) | Colors |
|-------|---------------------------|--------|
| **Knight** | Armor, helmet, sword/shield | Blue, silver, steel grey |
| **Mage** | Robe, staff, hood | Purple, violet, gold trim |
| **Rogue** | Dark cloak, hood, daggers | Black, dark grey, red accents |
| **Priest** | White robe, holy symbol, staff | White, gold, cream |
| **Adventurer** (default) | Mixed gear, traveler look | Brown, green, leather |

### 13.3 Avatar Display Rules

1. **Avatar size in UI:** 32×32px or 48×48px (multiples of 16).
2. **Avatar background:** Transparent — let the UI background show through.
3. **Avatar position:** Top of character card, centered.
4. **Fallback:** If no avatar is set, display a default pixel-adventurer icon.
5. **Avatar selector** (if implemented): Use the sprites from `asset/creting_cha_texture/character/` as options.
6. **Animation:** GIFs are supported for animated avatars (e.g. idle animation).

### 13.4 Character Placement Rules

1. **Dashboard:** Avatar in the character card header, stats below.
2. **Game screen:** Avatar in `.player-panel` (left sidebar on desktop).
3. **Full scene:** Walkers (8×12px) on the path are generic NPCs — not the player character.
4. **Do not place** large character illustrations as background elements — characters are data, not decoration.

---

## 14. Animation & Motion

### 14.1 Approved Animations

| Animation | Element | Duration | Timing |
|-----------|---------|----------|--------|
| `glow` | Game titles | 3s | `ease-in-out` infinite |
| `pulse-text` | Loading text | 1.5s | `ease-in-out` infinite |
| `sign-sway` | Wood sign | 5s | `ease-in-out` infinite |
| `cloud-drift` | Clouds | 40–55s | `linear` infinite |
| `sun-pulse` | Sun | 6s | `ease-in-out` infinite |
| `blades-spin` | Windmill blades | 8s | `linear` infinite |
| `window-glow` | House windows | 3s | `ease-in-out` infinite |
| `wheat-sway` | Wheat stalks | 4–5s | `ease-in-out` infinite |
| `walker-bob` | Walking NPCs | 0.4–0.45s | `ease-in-out` infinite |
| `walk-right` / `walk-left` | Walking NPCs | 18–24s | `linear` infinite |
| `scan` | CRT scanline overlay | 3s | `linear` infinite |

### 14.2 Animation Rules

1. **All animations must respect `prefers-reduced-motion: reduce`**:
   ```css
   @media (prefers-reduced-motion: reduce) {
       .animated-element {
           animation: none !important;
       }
   }
   ```
2. **Animations must use GPU-accelerated properties** only: `transform`, `opacity`, `box-shadow`, `text-shadow`. Never animate `width`, `height`, `margin`, `padding`, `top`, `left`.
3. **Scene animations** (clouds, windmill, wheat) are decorative — they should not distract from content.
4. **UI animations** (glow, pulse) should be subtle — max 3s cycle, small intensity change.
5. **No page transitions** (slide, fade between screens). Screens appear instantly.
6. **No loading spinners** — use the animated loading text instead (`pulse-text`).

---

## 15. Layout & Spacing System

### 15.1 Spacing Scale

| Token | Value | Usage |
|-------|-------|-------|
| `spacing-0` | 0px | None |
| `spacing-1` | 2px | Micro spacing |
| `spacing-2` | 4px | Extra small |
| `spacing-3` | 6px | Small |
| `spacing-4` | 8px | Small-medium |
| `spacing-5` | 10px | Medium-small |
| `spacing-6` | 12px | Medium |
| `spacing-7` | 14px | Medium-large |
| `spacing-8` | 15px | Panel padding |
| `spacing-9` | 16px | Large |
| `spacing-10` | 18px | Large + |
| `spacing-11` | 20px | Extra large |
| `spacing-12` | 24px | Section padding |
| `spacing-13` | 28px | Wood sign top padding |
| `spacing-14` | 30px | Container padding |
| `spacing-15` | 32px | Large section |
| `spacing-16` | 40px | Extra large |
| `spacing-17` | 48px | Massive |
| `spacing-18` | 52px | Chain height |
| `spacing-19` | 56px | House height |
| `spacing-20` | 64px | Sun size |

### 15.2 Layout Grid

| Breakpoint | Value | Layout Change |
|-----------|-------|---------------|
| `mobile` | ≤480px | Single column, reduced scene elements |
| `tablet` | 481–768px | Single column with normal padding |
| `desktop` | 769–1024px | Multi-column game layout |
| `wide` | >1024px | Max container constraints |

**Game screen grid (desktop):**
```css
.game-content {
    display: grid;
    grid-template-columns: 250px 1fr 150px;  /* player-panel | game-area | actions-panel */
    gap: 20px;
    max-width: 1000px;
}
```

**Game screen grid (mobile ≤ 768px):**
```css
@media (max-width: 768px) {
    .game-content {
        grid-template-columns: 1fr;  /* single column stack */
    }
}
```

### 15.3 Container Max Widths

| Container | Max Width | CSS |
|-----------|-----------|-----|
| App global | 1200px | `.container { max-width: 1200px }` |
| Wood sign | 420px | `.wood-sign { width: min(420px, 88vw) }` |
| Auth / Dashboard | 500px | `.auth-container / .dashboard-container { max-width: 500px }` |
| Game content | 1000px | `.game-content { max-width: 1000px }` |

---

## 16. Texture & Material Library

### 16.1 Material Textures (CSS-implemented)

| Material | CSS Technique | Used On |
|----------|--------------|---------|
| **Wood grain** | `repeating-linear-gradient` vertical lines on wood backgrounds | Wood signs, house doors |
| **Wood planks** | Vertical `repeating-linear-gradient` at 60px intervals | `.wood-sign-plank-lines` |
| **Chain links** | `repeating-linear-gradient` horizontal bands + left/right borders | `.sign-chain` |
| **CRT scanlines** | `repeating-linear-gradient` 2px rows | `.game-screen` overlay |
| **Wheat field** | `repeating-linear-gradient` vertical stripes + SVG wheat tile | `.pixel-wheat-field` |
| **Stone / brick** | (future) clip-path or box-shadow pixel blocks | Future dungeon screens |
| **Dirt path** | `repeating-linear-gradient` horizontal bands on trapezoid clip-path | `.pixel-path` |

### 16.2 Texture Usage Rules

1. **All textures are implemented in pure CSS** — no external images.
2. **Wood textures** are used for: signs, house doors, any "medieval wooden" UI element.
3. **Chain textures** are used ONLY for wood sign hangers.
4. **Scanlines** are used ONLY on game screens (`.game-screen`), not on auth/dashboard.
5. **Pixel scene textures** (wheat, path, sky) are used ONLY in pixel scene backgrounds.
6. **Never mix textures** — no wood grain on a metal chain, no scanlines on a wood sign.
7. **Texture opacity** must be subtle — `rgba(0,0,0,0.04)` to `rgba(0,0,0,0.1)` range.

---

## 17. Image & Illustration Rules

### 17.1 Pixel Art Standards

When creating or selecting images (especially for future AI image generation):

| Rule | Value |
|------|-------|
| **Color palette max** | 32 colors per image |
| **Resize algorithm** | Nearest neighbour (no anti-aliasing/blur) |
| **Edge style** | Pixel-perfect (crisp 1px edges) |
| **Outline** | 1px dark outline on foreground objects |
| **Background** | Transparent (for characters, icons, items) |
| **Canvas size** | Multiples of 16px (32×32, 48×48, 64×64, 128×128) |
| **File format** | PNG (static) or GIF (animated) — never JPG for pixel art |
| `image-rendering` | Always `pixelated` in CSS |

### 17.2 When to Use Images vs CSS

| Use Case | Preferred | Reason |
|----------|-----------|--------|
| Character avatars | PNG image | Real sprites from `asset/creting_cha_texture/character/` |
| Background scenes | CSS pixel art | Fully responsive, lighter, animatable |
| Dungeon / game art | PNG image | Complex detail beyond CSS capability |
| Icons (UI) | CSS-only | Consistent with pixel aesthetic |
| Decorations (nails, chains) | CSS pseudo-elements | Zero network cost |

### 17.3 File Naming for Images

- `kebab-case-descriptive-name.png`
- Include size in filename if variant-specific: `icon-sword-16x16.png`
- Group in subdirectories by type: `asset/icons/`, `asset/backgrounds/`, `asset/characters/`

---

## 18. CSS Naming Convention

### 18.1 Methodology

LifeQuest uses **BEM-lite** — a simplified Block Element Modifier with kebab-case.

| Pattern | Example |
|---------|---------|
| **Block** | `.wood-sign` |
| **Element** (double underscore) | `.wood-sign__title`, `.wood-sign__content` |
| **Modifier** (double hyphen) | `.wood-sign--active`, `.btn--disabled` |

### 18.2 Naming Rules

1. **Always use kebab-case** for CSS class names: `.game-screen`, `.player-panel`, `.pixel-cloud-1`.
2. **Never use camelCase** in CSS: use `.statRow` → `.stat-row`.
3. **Never use snake_case** in CSS: use `.user_name` → `.user-name`.
4. **State modifiers** use double hyphen: `.btn--disabled`, `.panel--collapsed`.
5. **JS hooks** use `.js-` prefix: `.js-toggle-inventory`, `.js-submit-form`.
6. **Utility classes** are lowercase with hyphens: `.text-center`, `.space-y-3`, `.flex-col`.

### 18.3 Selector Depth

- **Maximum depth:** 3 levels (e.g. `.wood-sign .btn-primary:hover`).
- **Prefer flat selectors** — avoid nesting more than 2 levels deep.
- **Avoid IDs in CSS** — use classes for styling, IDs only for JS targeting.
- **Never use `!important`** unless overriding a third-party library.

---

## 19. Accessibility

### 19.1 Minimum Standards

Even for a Telegram Mini App with a niche pixel-art audience, accessibility must be maintained:

| Rule | Value | Notes |
|------|-------|-------|
| **Touch target size** | Minimum 44×44px | For all interactive elements (buttons, links) |
| **Color contrast** | WCAG AA (4.5:1 text, 3:1 large text) | Test `#c0c0c0` on `#0a0e27` — passes (contrast ~9:1) |
| **Focus indicator** | Visible `:focus-visible` outline | Gold glow (`0 0 0 2px #d4af37`) — do NOT remove `outline` |
| **Keyboard navigation** | All interactive elements reachable via Tab | Test with keyboard before shipping |
| `aria-label` | Required on all icon-only/ambiguous elements | E.g. `<button aria-label="Close">✕</button>` |
| `role` attributes | Use semantic HTML first, `role` only as fallback | Prefer `<button>` over `role="button"` |
| **Reduced motion** | Respect `prefers-reduced-motion: reduce` | Turn off all infinite animations |
| **Form labels** | Every input must have a `<label>` | Use `for` attribute matching `id` |
| **Error announcements** | `aria-live="polite"` on error containers | Screen readers will announce errors |

### 19.2 Dark UI Specifics

- Text on `--primary-dark` (`#0a0e27`): `--text-primary` (`#c0c0c0`) → contrast ratio **~9.2:1** ✅
- Text on `--secondary-dark` (`#16213e`): `--text-primary` (`#c0c0c0`) → contrast ratio **~7.1:1** ✅
- Text on `--tertiary-dark` (`#1a1a2e`): `--text-primary` (`#c0c0c0`) → contrast ratio **~6.8:1** ✅
- Error text (`#f44336`) on `--primary-dark` → contrast ratio **~4.7:1** ✅
- Success text (`#4caf50`) on `--primary-dark` → contrast ratio **~4.6:1** ✅

### 19.3 Accessibility Checklist for New Screens

- [ ] All buttons are `<button>` elements (not `<div>`)
- [ ] All inputs have `<label>` with `for` attribute
- [ ] Touch targets are ≥44×44px
- [ ] Focus styles are visible
- [ ] Animations stop with `prefers-reduced-motion: reduce`
- [ ] Error messages use `aria-live="polite"`
- [ ] `aria-hidden="true"` on decorative pixel scene
- [ ] Tab navigation follows logical order

---

## 20. Forbidden UI

> These patterns are **STRICTLY FORBIDDEN** — they break the pixel-art dark fantasy aesthetic and/or Telegram Mini App constraints.

| ❌ Forbidden Pattern | Why It's Banned |
|---------------------|----------------|
| **Glassmorphism** (`backdrop-filter: blur`, transparent glass overlays) | Destroys pixel-art crispness |
| **Material Design** (elevation, ripple, floating labels) | Google style conflicts with medieval fantasy |
| **Large border-radius** (`border-radius: 8px+` on main UI) | Rounded corners break pixel-art feel |
| **Neon gradients** (cyberpunk pink/cyan/blue) | Wrong era — this is medieval, not cyberpunk |
| **Floating Action Buttons (FAB)** | Not a mobile-native pattern for this genre |
| **Hamburger menu** (three-line icon) | Forbidden in Telegram Mini Apps; use flat nav |
| **White backgrounds** (`background: #fff` anywhere) | Destroys dark fantasy atmosphere |
| **Bootstrap / Tailwind utility classes** | Generic frameworks dilute unique style |
| **iOS-style switches / toggles** | Too modern, breaks immersion |
| **Large / diffuse box-shadows** (> 20px spread) | Muddy on mobile, not pixel-friendly |
| **Blur effects** (`filter: blur()`) | Anti-aliased blur contradicts pixel art |
| **Gradient text** (`background-clip: text`) | Hard to read, conflicts with pixel font |
| **Animated backgrounds** (parallax, moving gradients) | Performance issues on low-end devices |
| **Loading spinners** | Use `pulse-text` animation instead |
| **Dropdown / select menus** | Poor mobile UX in Telegram; use button lists |
| **Bottom navigation bars** | Use Telegram Main Button (primary action) |
| **Skeuomorphic 3D elements** (excessive bevels, emboss) | Over-designed; keep pixel-flat |

---

## 21. Quick Reference Card

For AI agents generating new UI:

```
SCREEN TYPE → USE
─────────────────────────────────────────────────
welcome/loading/auth/error/settings/dashboard
  → Full or simplified pixel scene bg
  → Wood sign container (chains + plank board)
  → Pixel font (Press Start 2P)
  → Wood-edge colors, flat shadows

game/play/inventory/quests
  → Dark gradient bg (#0a0e27 → #16213e)
  → CRT scanline overlay
  → Dark panels (#1a1a2e) with gold border
  → Glowing titles and panels
  → Gold/red accent colors

BUTTON TYPE → WHEN
─────────────────────────────────────────────────
btn-primary (red)    → Primary actions, danger
btn-success (gold)   → Success, confirm, positive
btn-secondary (grey) → Secondary, cancel, back
wood btn-primary     → Green gradient on wood signs
wood btn-success     → Gold gradient on wood signs
wood btn-secondary   → Transparent on wood signs

COLOR QUICK CHART
─────────────────
Background     → #0a0e27
Surface        → #16213e
Panel          → #1a1a2e
Text           → #c0c0c0
Muted          → #808080
Gold accent    → #d4af37
Red accent     → #e94560
Border         → #404854
Wood edge      → #4a2e18
Wood mid       → #a06840

ACCESSIBILITY BASICS
────────────────────
Touch target   → 44×44px minimum
Focus style    → Gold outline (never remove)
Motion         → Test with prefers-reduced-motion
Contrast       → AA minimum (4.5:1 text)
Labels         → Every input needs <label>
Semantic HTML  → <button> not <div>

FORBIDDEN (never use)
──────────────────────
✗ Glassmorphism      ✗ Material Design
✗ Large border-radius ✗ Neon gradients
✗ White backgrounds  ✗ Hamburger menus
✗ Blur effects       ✗ Loading spinners
✗ Bottom nav bars    ✗ Dropdown menus
```

> **End of UI Style Guide.**  
> Any AI agent modifying or extending the LifeQuest UI MUST use this document as the single source of truth for visual decisions.  
> If a rule in this document conflicts with an external design trend, the rule wins.
>  
> **Priority:** `design_tokens.json` > `ui_style.md` > `components.md`  
> **Component lookup:** Button → `components.md` | WoodSign → `components.md` | Card → `components.md`

