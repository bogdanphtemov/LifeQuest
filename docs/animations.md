# LifeQuest — Animation System

> **Canonical source:** This document defines every animation, transition, and motion behaviour in the project.  
> **Priority:** `design_tokens.json` > `ui_style.md` > `animations.md` (this file).  
> **AI agents:** All motion values must be referenced from here. Never hardcode animation durations or easing functions.

---

## Table of Contents

1. [Core Principles](#1-core-principles)
2. [Animation Quick Reference](#2-animation-quick-reference)
3. [Hover & Focus Animations](#3-hover--focus-animations)
4. [Click / Active Animations](#4-click--active-animations)
5. [Screen Transitions](#5-screen-transitions)
6. [Loading Animations](#6-loading-animations)
7. [Scene / Background Animations](#7-scene--background-animations)
8. [Modal Animations](#8-modal-animations)
9. [Card & Panel Animations](#9-card--panel-animations)
10. [Menu Animations](#10-menu-animations)
11. [Entrance Animations](#11-entrance-animations)
12. [Exit Animations](#12-exit-animations)
13. [Reduced Motion](#13-reduced-motion)
14. [Performance Guidelines](#14-performance-guidelines)
15. [Animation Token Reference](#15-animation-token-reference)
16. [Animation Composition](#16-animation-composition)
17. [Animation Events](#17-animation-events)
18. [State Machine](#18-state-machine)
19. [Testing Guidelines](#19-testing-guidelines)
20. [Browser Support](#20-browser-support)

---

## 1. Core Principles

### 1.1 Design Philosophy

Animations in LifeQuest follow the **pixel-art RPG** aesthetic — they should feel chunky, deliberate, and slightly retro. This means:

| Principle | Rule | Reason |
|-----------|------|--------|
| **Subtle** | Never purely decorative; animatations must serve a functional purpose | Mimics classic 16-bit RPGs |
| **Fast** | 0.1s–0.4s for interaction feedback | Feels responsive, not sluggish |
| **Chunky** | Use `ease-in-out` or `linear` — avoid bouncy/spring easings | Pixel aesthetic demands mechanical feel |
| **Discrete** | Elements animate in distinct steps where possible | Avoids modern "smooth" UI feel |
| **Respectful** | Must respect `prefers-reduced-motion: reduce` | Accessibility requirement |

### 1.2 Global Defaults

```css
:root {
    /* Transition defaults — always use specific properties, never `all` */
    --transition-fast: opacity 0.3s ease, transform 0.3s ease, background-color 0.3s ease, box-shadow 0.3s ease;

    /* Duration tokens */
    --duration-instant: 0.1s;
    --duration-fast: 0.3s;
    --duration-normal: 0.4s;
    --duration-slow: 1.5s;

    /* Timing functions */
    --ease-default: ease;
    --ease-in-out: ease-in-out;
    --ease-linear: linear;
}

/* ⚠️ `transition: all` is forbidden in production code.
   Always list animated properties explicitly to prevent:
   - Accidental animation of unintended properties
   - Performance degradation from unnecessary GPU work
*/

### 1.3 CSS Custom Properties for Animation

All animation values **must** use these tokens. Hardcoding values is forbidden.

**Duration tokens** (from `design_tokens.json` → `animation.duration`):

| Token | Value | Used For |
|-------|-------|----------|
| `instant` | `0.1s` | Button press, active states |
| `fast` | `0.3s` | Hover, focus, transition toggles |
| `normal` | `0.4s` | Walker bob, modal entrance |
| `slow` | `1.5s` | Loading pulse |
| `scene.glow` | `3s` | Title glow, window glow, scanline |
| `scene.sway` | `4s` | Wheat sway |
| `scene.signSway` | `5s` | Hanging wood sign |
| `scene.sunPulse` | `6s` | Sky sun pulsing |
| `scene.blades` | `8s` | Windmill blades spin |
| `scene.walkerFast` | `18s` | Walker 1 (right) |
| `scene.walkerSlow` | `24s` | Walker 2 (right, slow) |
| `scene.walkerLeft` | `22s` | Walker 3 (left) |
| `scene.cloudFast` | `40s` | Cloud 1 drift |
| `scene.cloudSlow` | `55s` | Cloud 2 drift |

> **Token naming convention:** Duration tokens follow a hierarchical pattern:
> - `instant`, `fast`, `normal`, `slow` — for interaction/transition speed
> - `scene.*` — for continuous background/scene animations
> - `modal.*`, `screen.*` — (future) for modal and screen transitions
>
> This keeps the design system scalable: new scene animations always use `scene.<name>` prefix.

**Timing function tokens** (from `design_tokens.json` → `animation.timingFunction`):

| Token | Value | Used For |
|-------|-------|----------|
| `linear` | `linear` | Walkers, clouds, blades, scanlines |
| `ease` | `ease` | Default transitions |
| `ease-in-out` | `ease-in-out` | Glow, sway, pulse, bob |

---

## 2. Animation Quick Reference

| # | Animation | CSS Keyframe(s) | Duration | Easing | Element | Category |
|---|-----------|-----------------|----------|--------|---------|----------|
| 1 | `button-hover` | — (transition) | 0.3s | ease | `.btn` | Hover/Focus |
| 2 | `button-active-dark` | — (transform) | 0.1s | ease | `.btn:active` (dark UI) | Click/Active |
| 3 | `button-active-wood` | — (transform + shadow) | 0.1s | ease | `.btn:active` (wood sign) | Click/Active |
| 4 | `input-focus` | — (transition) | 0.3s | ease | `.form-input` | Hover/Focus |
| 5 | `loading-pulse` | `pulse-text` | 1.5s | ease-in-out | `.loading-text` | Loading |
| 6 | `title-glow` | `glow` | 3s | ease-in-out | `.game-screen .game-title` | Scene |
| 7 | `scanline` | `scan` | 3s | linear | `.game-screen::before` | Scene |
| 8 | `sun-pulse` | `sun-pulse` | 6s | ease-in-out | `.pixel-sun` | Scene |
| 9 | `cloud-drift-1` | `cloud-drift` | 40s | linear | `.pixel-cloud-1` | Scene |
| 10 | `cloud-drift-2` | `cloud-drift` | 55s | linear | `.pixel-cloud-2` (reverse) | Scene |
| 11 | `blades-spin` | `blades-spin` | 8s | linear | `.windmill-blades` | Scene |
| 12 | `window-glow` | `window-glow` | 3s | ease-in-out | `.house-window` | Scene |
| 13 | `wheat-sway` | `wheat-sway` | 4s | ease-in-out | `.wheat-stalks` | Scene |
| 14 | `wheat-sway-2` | `wheat-sway` | 5s | ease-in-out | `.wheat-stalks-2` (reverse) | Scene |
| 15 | `walker-bob` | `walker-bob` | 0.4s | ease-in-out | `.pixel-walker` | Scene |
| 16 | `walk-right-1` | `walk-right` | 18s | linear | `.walker-1` | Scene |
| 17 | `walk-right-2` | `walk-right` | 24s | linear | `.walker-2` | Scene |
| 18 | `walk-left` | `walk-left` | 22s | linear | `.walker-3` | Scene |
| 19 | `sign-sway` | `sign-sway` | 5s | ease-in-out | `.sign-hanger` | Scene |
| 20 | `screen-switch` | — (future) | 0.2s | ease | `.screen` | Screen Transition |
| 21 | `modal-enter` | — (future) | 0.2s | ease | `.modal-overlay` | Modal |
| 22 | `modal-exit` | — (future) | 0.15s | ease | `.modal-overlay` | Modal |
| 23 | `progress-fill` | — (future) | 0.5s | ease | `.progress-bar__fill` | Card/Panel |
| 24 | `card-enter` | — (future) | 0.3s | ease | `.character-card` | Entrance |
| 25 | `menu-open` | — (future) | 0.2s | ease | `.menu` | Menu |

---

## 3. Hover & Focus Animations

### 3.1 Button Hover

**Affects:** `.btn-primary`, `.btn-success`, `.btn-secondary`  
**Duration:** `0.3s`  
**Easing:** `ease`  
**Performance:** Uses `background-color` + `box-shadow` (GPU composited)

```
┌─────────────────────────────────────┐
│                                     │
│    dark UI:     bg: transparent     │
│                 → rgba(accent, 0.2) │
│                 shadow: none        │
│                 → 0 0 15px glow     │
│                                     │
│    wood sign:   bg: gradient        │
│                 → brighter gradient │
│                 shadow: deeper      │
│                                     │
└─────────────────────────────────────┘
```

**CSS implementation:**

```css
.btn-primary {
    background-color: transparent;
    color: var(--accent-red);
    transition: background-color var(--duration-fast) var(--ease-default),
                box-shadow var(--duration-fast) var(--ease-default),
                color var(--duration-fast) var(--ease-default),
                transform var(--duration-instant) var(--ease-default);
}

.btn-primary:hover {
    background-color: rgba(233, 69, 96, 0.2);
    box-shadow: 0 0 15px rgba(233, 69, 96, 0.4);
}
```

**Wood sign variant:**

```css
.wood-sign .btn-primary {
    background: linear-gradient(180deg, #6a9a40, #4a7a28);
    box-shadow: 0 4px 0 #2a5018, 0 6px 12px rgba(0,0,0,0.3);
    transition: background var(--duration-fast) var(--ease-default),
                box-shadow var(--duration-fast) var(--ease-default),
                transform var(--duration-instant) var(--ease-default);
}

.wood-sign .btn-primary:hover {
    background: linear-gradient(180deg, #7aaa50, #5a8a38);
    box-shadow: 0 4px 0 #2a5018, 0 8px 16px rgba(0,0,0,0.35);
}
```

### 3.2 Input Focus

**Affects:** `.form-input`  
**Duration:** `0.3s`  
**Easing:** `ease`  
**Performance:** Uses `border-color` + `box-shadow` (GPU composited)

```
┌─────────────────────────────────┐
│ default:   border: #404854      │
│            bg: #16213e          │
│            shadow: none         │
│                                 │
│ focus:     border: #d4af37      │
│            bg: rgba(22,33,62,.8)│
│            shadow: 0 0 10px     │
│            rgba(212,175,55,.3)  │
└─────────────────────────────────┘
```

**CSS implementation:**

```css
.form-input {
    transition: border-color var(--duration-fast) var(--ease-default),
                box-shadow var(--duration-fast) var(--ease-default),
                background-color var(--duration-fast) var(--ease-default);
}

.form-input:focus {
    border-color: var(--accent-gold);
    box-shadow: 0 0 10px rgba(212, 175, 55, 0.3);
    background-color: rgba(22, 33, 62, 0.8);
}
```

---

## 4. Click / Active Animations

### 4.1 Button Active (Dark UI)

**Affects:** `.btn:active` (outside `.wood-sign`)  
**Duration:** `0.1s`  
**Easing:** `ease`  
**Transform:** `scale(0.98)` — simulates mechanical button press

```
┌───────────────────────┐
│  idle        pressed  │
│  ┌─────┐     ┌─────┐ │
│  │ BTN │ →   │ BTN │ │
│  └─────┘     └─────┘ │
│  scale: 1    scale:.98│
└───────────────────────┘
```

```css
.btn:active {
    transform: scale(0.98);
}
```

### 4.2 Button Active (Wood Sign)

**Affects:** `.btn:active` inside `.wood-sign`  
**Duration:** `0.1s`  
**Easing:** `ease`  
**Transform:** `translateY(3px)` — simulates pushing a physical wooden button downward  
**Shadow:** All 3D `box-shadow` replaced with `0 1px 0 var(--wood-edge)`

```
┌──────────────────────────┐
│  idle            pressed │
│  ┌─────────┐    ┌────────│
│  │  BTN    │    │        │
│  │█████████│ →  │  BTN   │
│  │  shadow │    │  │     │
│  └─────────┘    └──│─────│
│                    shadow │
│  translateY: 0    +3px   │
└──────────────────────────┘
```

```css
.wood-sign .btn:active {
    transform: translateY(3px);
    box-shadow: 0 1px 0 var(--wood-edge) !important;
}
```

### 4.3 No Double-Tap Zoom

All interactive elements must disable double-tap zoom on mobile:

```css
.btn, .form-input, a {
    touch-action: manipulation;
}
```

---

## 5. Screen Transitions

### 5.1 Screen Switch

**Affects:** `.screen` → `.screen.active`  
**Current:** Instant (no animation)  
**Duration (proposed):** `0.2s`  
**Easing (proposed):** `ease`

**Current implementation** (no animation — instant swap):

```javascript
function hideAllScreens() {
    document.querySelectorAll('.screen').forEach(function (screen) {
        screen.classList.remove('active');
    });
}
```

**Proposed future implementation** (fade transition):

```css
.screen {
    transition: opacity var(--duration-fast) ease, visibility var(--duration-fast) ease;
    opacity: 0;
    visibility: hidden;
}

.screen.active {
    opacity: 1;
    visibility: visible;
}
```

**Why instant currently:** The Telegram Mini App must feel fast. Animating screen transitions adds 200ms latency. If animations are added, use `opacity` only (cheap for GPU) and keep duration ≤ 200ms.

### 5.2 Screen Type Differences

| Screen | Enter Animation | Exit Animation | Notes |
|--------|----------------|----------------|-------|
| Loading → Dashboard | Instant (current) / Fade (future) 0.2s | Instant | Critical path — must be fast |
| Loading → Error | Instant | Instant | Error states must appear immediately |
| Dashboard → Game | (future) Fade 0.2s | (future) Fade 0.15s | Future game screens — only fade allowed |

### 5.3 Transition Rules

1. **Only fade** between screens — no slides, no 3D flips, no scaling. **This rule is absolute:** slides would break the pixel-scene illusion and add complexity.
2. **Never use `transform`** for screen transitions (risks z-index layer issues with pixel scene).
3. **Duration:** 0.15s–0.2s max. The RPG pixel art aesthetic demands snappy transitions.
4. **`will-change: opacity`** on `.screen.active` for GPU acceleration.

---

## 6. Loading Animations

### 6.1 Loading Text Pulse

**Affects:** `.loading-text`  
**Keyframe:** `pulse-text`  
**Duration:** `1.5s`  
**Easing:** `ease-in-out infinite`  
**Property:** `opacity`

```
opacity
  1.0 ─╮      ╱╲      ╱╲
  0.9   ╱    ╱  ╲    ╱  ╲
  0.8  ╱   ╱    ╲  ╱    ╲
  0.7 ╱  ╱      ╲╱      ╲
  0.6╱ ╱                 ╲
      ──────┬──────┬──────┬──── time
           0.75s   1.5s   2.25s
```

```css
@keyframes pulse-text {
    0%, 100% { opacity: 0.6; }
    50% { opacity: 1; }
}

.loading-text {
    animation: pulse-text 1.5s ease-in-out infinite;
}
```

### 6.2 Loading State (Button)

**Affects:** Any `.btn.loading`  
**Duration:** Instant (class toggle)  
**Properties:** `opacity: 0.6`, `pointer-events: none`

Not an animation per se — a static disabled visual state. The loading button does not spin or show a spinner. Text changes to indicate progress.

```css
.loading {
    opacity: 0.6;
    pointer-events: none;
}
```

---

## 7. Scene / Background Animations

### 7.1 Title Glow

**Affects:** `.game-screen .game-title`  
**Keyframe:** `glow`  
**Duration:** `3s`  
**Easing:** `ease-in-out infinite`  
**Property:** `text-shadow`

```
Text-shadow intensity over time:

  glow        ───────────────
  intensity   ╱              ╲
             ╱                ╲
            ╱                  ╲
  normal    ╱                    ╲
            ────┬────┬────┬────┬──
               0.75  1.5  2.25  3s

  Start:  gold 10px + red 20px
  Mid:    gold 20px + red 30px
  End:    gold 10px + red 20px
```

```css
@keyframes glow {
    0%, 100% {
        text-shadow:
            2px 2px 4px rgba(0, 0, 0, 0.8),
            0 0 10px rgba(212, 175, 55, 0.5),
            0 0 20px rgba(233, 69, 96, 0.3);
    }
    50% {
        text-shadow:
            2px 2px 4px rgba(0, 0, 0, 0.8),
            0 0 20px rgba(212, 175, 55, 0.8),
            0 0 30px rgba(233, 69, 96, 0.5);
    }
}
```

### 7.2 Scanline Overlay

**Affects:** `.game-screen::before`  
**Keyframe:** `scan`  
**Duration:** `3s`  
**Easing:** `linear infinite`  
**Property:** `transform: translateY`

```
┌─────────────────────────┐
│   ░░░░░░░░░░░░░░░░░░░   │  ← scanlines move
│   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   │     downward at
│   ░░░░░░░░░░░░░░░░░░░   │     2px/s
│   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   │
│   ░░░░░░░░░░░░░░░░░░░   │
│   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   │
│   ░░░░░░░░░░░░░░░░░░░   │
└─────────────────────────┘
     translateY: 0 → 4px
```

```css
@keyframes scan {
    0% { transform: translateY(0); }
    100% { transform: translateY(4px); }
}

.game-screen::before {
    animation: scan 3s linear infinite;
}
```

**Reduced motion:** Entire `::before` pseudo-element is removed when `prefers-reduced-motion: reduce`.

> **Subtlety note:** The scanline moves only 4px over 3 seconds (≈1.3px/s). This is deliberately subtle — it adds
> ambiance without being noticeable during normal use. The motion should **never** be sped up to resemble
> CRT flicker or interlaced video, which can trigger migraines or epilepsy in sensitive users.

### 7.3 Sun Pulse

**Affects:** `.pixel-sun`  
**Keyframe:** `sun-pulse`  
**Duration:** `6s`  
**Easing:** `ease-in-out infinite`  
**Properties:** `transform: scale`, `opacity`

```
Sun
size    ╱───╲     ╱───╲
1.05x  ╱     ╲   ╱     ╲
1.00x ╱       ╲╱         ╲
      ────┬────┬────┬────┬── time
         1.5   3    4.5   6s
```

```css
@keyframes sun-pulse {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.05); opacity: 0.92; }
}
```

### 7.4 Cloud Drift

**Affects:** `.pixel-cloud-1`, `.pixel-cloud-2`  
**Keyframe:** `cloud-drift`  
**Durations:** 40s (cloud 1), 55s (cloud 2)  
**Easing:** `linear infinite`  
**Property:** `transform: translateX`

```
Cloud 1:  translateX: 0 → 60px  (40s, →)
Cloud 2:  translateX: 0 → 60px  (55s, ← reverse)
```

```css
@keyframes cloud-drift {
    0% { transform: translateX(0); }
    100% { transform: translateX(60px); }
}

.pixel-cloud-1 {
    animation: cloud-drift 40s linear infinite;
}

.pixel-cloud-2 {
    animation: cloud-drift 55s linear infinite reverse;
}
```

### 7.5 Windmill Blades

**Affects:** `.windmill-blades`  
**Keyframe:** `blades-spin`  
**Duration:** `8s`  
**Easing:** `linear infinite`  
**Property:** `transform: rotate`
**transform-origin:** `center center` (must be set explicitly for cross-browser consistency)

```
0° → 360° continuous rotation at 45°/s
```

```css
@keyframes blades-spin {
    from { transform: translateX(-50%) rotate(0deg); }
    to { transform: translateX(-50%) rotate(360deg); }
}

.windmill-blades {
    transform-origin: center center;
    animation: blades-spin 8s linear infinite;
}
```

### 7.6 Window Glow (House)

**Affects:** `.house-window`  
**Keyframe:** `window-glow`  
**Duration:** `3s`  
**Easing:** `ease-in-out infinite`  
**Property:** `opacity`

```
opacity
1.0 ────────────────╮
                    ╲
0.9                  ╲
0.8                    ╲
0.7                     ╲─────────────
      ─────┬────┬────┬────┬────┬────
          0.75  1.5  2.25  3    3.75s
```

```css
@keyframes window-glow {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}
```

### 7.7 Wheat Sway

**Affects:** `.wheat-stalks`, `.wheat-stalks-2`  
**Keyframe:** `wheat-sway`  
**Durations:** 4s (stalks 1), 5s (stalks 2, reversed)  
**Easing:** `ease-in-out infinite`  
**Property:** `transform: skewX`

```
     idle               sway
  ╱   ╲   ╱          ╱    ╲  ╱
 ╱     ╲ ╱    →     ╱      ╲╱
╱       ╲          ╱
         ╲        ╱          ╲
          ╲      ╱            ╲
  skewX: 0°      skewX: 1.5° (then back)
```

```css
@keyframes wheat-sway {
    0%, 100% { transform: skewX(0deg); }
    50% { transform: skewX(1.5deg); }
}

.wheat-stalks {
    animation: wheat-sway 4s ease-in-out infinite;
}

.wheat-stalks-2 {
    animation: wheat-sway 5s ease-in-out infinite reverse;
    animation-delay: -1s;
}
```

### 7.8 Walker Bob

**Affects:** All `.pixel-walker` elements  
**Keyframe:** `walker-bob`  
**Duration:** 0.4s–0.45s (per walker)  
**Easing:** `ease-in-out infinite`  
**Property:** `transform: translateY`

```
Vertical bobbing while walking:
    Y    ╱╲    ╱╲
   -2   ╱  ╲  ╱  ╲
    0  ╱    ╲╱    ╲
       0  0.2  0.4  0.6s
```

```css
@keyframes walker-bob {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-2px); }
}
```

> **Composition note:** `walker-bob` is combined with `walk-right`/`walk-left` on the same element.
> See [Animation Composition](#16-animation-composition) for how multiple keyframes on one element work.

### 7.9 Walker Horizontal Movement

**Affects:** `.walker-1`, `.walker-2`, `.walker-3`  
**Keyframes:** `walk-right`, `walk-left`  
**Durations:** 18s, 24s, 22s  
**Easing:** `linear infinite`  
**Property:** `transform: translateX` (via wrapper) + `opacity`

> **Why `translateX` instead of `left`/`right`:** `transform` is GPU-composited and avoids layout recalculations.
> The walkers use a **wrapper element** (`.walker-wrapper`) positioned with `left`/`right` statically,
> and the animation runs on `transform: translateX()` inside it.

```
Walker 1:  translateX(-80px → +80px)  (18s, →, 4s delay)
Walker 2:  translateX(-80px → +80px)  (24s, →, 12s delay)
Walker 3:  translateX(+80px → -80px)  (22s, ←, 8s delay)

Fade in/out at edges via opacity:
  0%  →  8%   →  92%  → 100%
  opacity: 0 →  1   →   1    →  0
```

```css
/* Wrapper: positioned with static left/right (no animation) */
.walker-1 { left: 0%; }
.walker-2 { left: 0%; }
.walker-3 { right: 0%; }

/* Animation on transform only */
@keyframes walk-right {
    0%   { transform: translateX(-80px); opacity: 0; }
    8%   { opacity: 1; }
    92%  { opacity: 1; }
    100% { transform: translateX(80px); opacity: 0; }
}

@keyframes walk-left {
    0%   { transform: translateX(80px); opacity: 0; }
    8%   { opacity: 1; }
    92%  { opacity: 1; }
    100% { transform: translateX(-80px); opacity: 0; }
}

/* Composition: each walker has TWO animations (bob + horizontal) */
.walker-1 {
    animation:
        walk-right 18s linear infinite 4s,
        walker-bob 0.4s ease-in-out infinite;
}

.walker-2 {
    animation:
        walk-right 24s linear infinite 12s,
        walker-bob 0.45s ease-in-out infinite;
}

.walker-3 {
    animation:
        walk-left 22s linear infinite 8s,
        walker-bob 0.42s ease-in-out infinite;
}
```

> **Animation composition rules:** When multiple animations target the same property (e.g., `transform`),
> the last animation in the shorthand wins for that property. `walker-bob` and `walk-right` both use
> `transform`, so `walker-bob` must appear **second** to layer on top without overwriting the horizontal position.
> See [Animation Composition](#16-animation-composition) for details.

### 7.10 Wood Sign Sway

**Affects:** `.sign-hanger`  
**Keyframe:** `sign-sway`  
**Duration:** `5s`  
**Easing:** `ease-in-out infinite`  
**Property:** `transform: rotate`
**transform-origin:** `top center` (the sign hangs from the top; rotation must originate from the hanging point)

```
     idle ──── left ──── right ──── idle
        │      ╱╲      ╱╲
  0.6°  │     ╱  ╲    ╱  ╲
   0°   │    ╱    ╲  ╱    ╲
 -0.6°  │   ╱      ╲╱      ╲
        └───┬──────┬──────┬────── time
           1.25   2.5    3.75   5s
```

```css
@keyframes sign-sway {
    0%, 100% { transform: rotate(-0.6deg); }
    50% { transform: rotate(0.6deg); }
}

.sign-hanger {
    transform-origin: top center;
    animation: sign-sway 5s ease-in-out infinite;
}
```

### 7.11 Vignette Overlay (Static)

**Affects:** `.auth-screen::after`  
**Duration:** None (static gradient)  
**Property:** `background: radial-gradient`

```
        ┌─────────────────┐
        │   ▓▓░░░░░░░▓▓   │
        │ ▓░░░░░░░░░░░░▓  │  ← Dark corners, transparent
        │ ░░░░░░░░░░░░░░  │     center at 40% height
        │ ▓░░░░░░░░░░░░▓  │
        │   ▓▓░░░░░░░▓▓   │
        └─────────────────┘
```

This is not an animation — it's a static vignette for depth. Listed here because it's part of the visual effect system.

---

## 8. Modal Animations

### 8.1 Modal Open (Future Implementation)

**Affects:** `.modal-overlay` → `.modal-overlay.open`  
**Duration:** `0.2s`  
**Easing:** `ease`  
**Properties:** `opacity` (overlay), `transform: translateY` + `opacity` (content)

**Proposed timeline:**

```
0ms    overlay: opacity 0 → 1
30ms   content: translateY(20px → 0), opacity 0 → 1
200ms  Complete
```

**Proposed CSS:**

```css
.modal-overlay {
    opacity: 0;
    transition: opacity 0.2s ease;
    pointer-events: none;
}

.modal-overlay.open {
    opacity: 1;
    pointer-events: auto;
}

.modal-content {
    transform: translateY(20px);
    opacity: 0;
    transition: transform 0.2s ease, opacity 0.2s ease;
}

.modal-overlay.open .modal-content {
    transform: translateY(0);
    opacity: 1;
}
```

### 8.2 Modal Close (Future Implementation)

**Duration:** `0.15s`  
**Direction:** Reverse of open  
**Properties:** Same as open, but faster (50% of open time)

```
0ms    content: translateY(0 → 10px), opacity 1 → 0
50ms   overlay: opacity 1 → 0
150ms  Complete → display: none
```

### 8.3 Modal Rules

1. **Overlay fade only** — no blur effects (forbidden by `frontend_rules.md`).
2. **Content slides up** 20px — not down, not scale.
3. **No bouncy easings** — use `ease`, not `cubic-bezier` overshoot.
4. **`aria-modal="true"`** must be set when open.
5. **Focus trap:** First focusable element receives focus on open.

---

## 9. Card & Panel Animations

### 9.1 CharacterCard Entrance (Future Implementation)

**Affects:** `.character-card` on dashboard load  
**Duration:** `0.3s`  
**Easing:** `ease`  
**Properties:** `opacity` + `transform: translateY`

```
Before:   opacity: 0, translateY(10px)
After:    opacity: 1, translateY(0)
Delay:    0.1s (stat rows stagger: 0.1s, 0.15s, 0.2s...)
```

```css
.character-card {
    animation: card-enter 0.3s ease forwards;
}

@keyframes card-enter {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
```

**Stat row stagger** (proposed for future):

```css
.stat-row:nth-child(1) { animation-delay: 0ms; }
.stat-row:nth-child(2) { animation-delay: 50ms; }
.stat-row:nth-child(3) { animation-delay: 100ms; }
/* ... */
```

### 9.2 ProgressBar Fill (Future Implementation)

**Affects:** `.progress-bar__fill`  
**Duration:** `0.5s`  
**Easing:** `ease`  
**Property:** `width` (set via inline style or CSS custom property)

```
width: 0% → 75%  (0.5s ease)
```

```css
.progress-bar__fill {
    transition: width 0.5s ease;
}
```

### 9.3 Panel Glow (Passive)

**Affects:** `.game-screen .player-panel`, `.game-screen .game-area`, `.game-screen .actions-panel`  
**Duration:** Static (not animated)  
**Properties:** `box-shadow`

The gold/red glow on game panels is a **static shadow**, not an animation. It does not pulse or change.

```css
.game-screen .player-panel {
    box-shadow:
        0 0 10px rgba(212, 175, 55, 0.3),
        0 0 20px rgba(233, 69, 96, 0.2),
        inset 0 0 10px rgba(212, 175, 55, 0.1);
}
```

---

## 10. Menu Animations

### 10.1 Actions Panel Button Stack (Future Implementation)

**Affects:** Buttons inside `.actions-panel`  
**Duration:** `0.2s` stagger  
**Easing:** `ease`  
**Properties:** `opacity` + `transform: translateX`

```
   ┌────────────────┐
   │ ▓▓▓  Quest     │  ← appears first (0ms)
   │ ▓▓▓  Inventory │  ← appears at 50ms
   │ ▓▓▓  Settings  │  ← appears at 100ms
   │ ▓▓▓  Logout    │  ← appears at 150ms
   └────────────────┘
   
   translateX(-10px → 0), opacity(0 → 1)
```

```css
.actions-panel .btn {
    animation: menu-item-enter 0.2s ease forwards;
    opacity: 0;
    transform: translateX(-10px);
}

.actions-panel .btn:nth-child(1) { animation-delay: 0ms; }
.actions-panel .btn:nth-child(2) { animation-delay: 50ms; }
.actions-panel .btn:nth-child(3) { animation-delay: 100ms; }
.actions-panel .btn:nth-child(4) { animation-delay: 150ms; }

@keyframes menu-item-enter {
    to {
        opacity: 1;
        transform: translateX(0);
    }
}
```

### 10.2 Menu Rules

1. **No hamburger menus** (forbidden by `frontend_rules.md`).
2. **Slide from left** — not right, not top, not bottom.
3. **Stagger delay:** 50ms between items, max 4 items.
4. **No submenu animations** — only top-level items.

---

## 11. Entrance Animations

### 11.1 Page / Screen Load

| Element | Animation | Duration | Delay |
|---------|-----------|----------|-------|
| `.wood-sign` | `opacity 0→1` + `translateY(10px→0)` | 0.3s | 0ms |
| `.game-title` | `opacity 0→1` | 0.2s | 50ms |
| `.game-subtitle` | `opacity 0→1` | 0.2s | 100ms |
| `.character-card` | `opacity 0→1` + `translateY(10px→0)` | 0.3s | 150ms |
| `.stat-row` (each) | `opacity 0→1` | 0.2s | 200ms + 50ms stagger |
| `.dashboard-note` | `opacity 0→1` | 0.3s | 400ms |

### 11.2 Element Entrance (Generic)

For any element that appears dynamically:

```css
.entrance-fade {
    animation: entrance-fade 0.3s ease forwards;
}

@keyframes entrance-fade {
    from {
        opacity: 0;
        transform: translateY(5px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
```

### 11.3 Entrance Rules

1. **Fade + slight slide** (5–10px) is the only allowed entrance pattern.
2. **No scale entrance** — elements should not grow from 0.
3. **No rotation entrance** — elements should not spin in.
4. **Stagger max:** 5 elements, 50ms apart.

---

## 12. Exit Animations

### 12.1 Element Exit (Generic)

For any element that disappears:

```css
.exit-fade {
    animation: exit-fade 0.15s ease forwards;
}

@keyframes exit-fade {
    from {
        opacity: 1;
        transform: translateY(0);
    }
    to {
        opacity: 0;
        transform: translateY(5px);
    }
}
```

### 12.2 Exit Rules

1. **Exit is 50% faster than entrance** (0.15s vs 0.3s).
2. **Fade + slight slide** downward (5px).
3. **No scale exit** — elements should not shrink to 0.
4. **No rotation exit.**

### 12.3 Exit Durations

| Element | Duration | Direction |
|---------|----------|-----------|
| Modal overlay | 0.15s | Fade out |
| Modal content | 0.15s | translateY(0→10px) |
| Screen (future) | 0.15s | Fade out |
| Message | 0.15s | Fade out |
| Tooltip (future) | 0.1s | Fade out |

---

## 13. Reduced Motion

### 13.1 Global Rule

Every single animation in this project **must** be disabled when the user has enabled `prefers-reduced-motion: reduce` in their OS settings.

### 13.2 Implementation

```css
@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation: none !important;
        transition: none !important;
        scroll-behavior: auto !important;
    }
}
```

> **Why `animation: none !important; transition: none !important;` instead of just setting `duration: 0.01ms`:**
> Some browsers still fire `transitionstart`/`transitionend` events even with near-zero durations, which can
> cause JavaScript listeners to fire unexpectedly. `none` completely removes the animation/transition lifecycle.

This blanket rule is acceptable for reducing all motion. However, for **scene animations that are purely decorative**, the `pixel-scene.css` uses a more targeted approach:

```css
@media (prefers-reduced-motion: reduce) {
    .pixel-windmill .windmill-blades,
    .pixel-walker,
    .sign-hanger,
    .wheat-stalks,
    .pixel-sun,
    .pixel-cloud-1,
    .pixel-cloud-2 {
        animation: none !important;
    }
}
```

### 13.3 Affected Animations Checklist

| Animation | Stopped? | Method |
|-----------|----------|--------|
| `pulse-text` (loading) | ✅ | Global rule |
| `glow` (title) | ✅ | Global rule |
| `scan` (scanlines) | ✅ | `::before` removed (`animation: none`) |
| `sun-pulse` | ✅ | Targeted `animation: none` |
| `cloud-drift` | ✅ | Targeted `animation: none` |
| `blades-spin` | ✅ | Targeted `animation: none` |
| `window-glow` | ✅ | Global rule |
| `wheat-sway` | ✅ | Targeted `animation: none` |
| `walker-bob` | ✅ | Targeted `animation: none` |
| `walk-right/left` | ✅ | Targeted `animation: none` |
| `sign-sway` | ✅ | Targeted `animation: none` |
| `button-hover` | ✅ | Global rule |
| `button-active` | ✅ | Global rule (hover → none) |
| `input-focus` | ✅ | Global rule |
| Modal enter/exit | ✅ | Global rule |

---

## 14. Performance Guidelines

### 14.1 GPU-Accelerated Properties: Allowed vs. Forbidden

**General rule:** Use `transform` and `opacity` for all keyframe animations. These are GPU-composited and do not trigger layout or paint.

| ✅ GPU (no layout/paint) | ⚠️ Allowed only as transitions | ❌ Forbidden in keyframes |
|--------------------------|-------------------------------|--------------------------|
| `opacity` | `background-color` (hover/focus transitions only) | `background-color` (continuous keyframe) |
| `transform: translate()` | `box-shadow` (hover/focus transitions only) | `box-shadow` (continuous keyframe) |
| `transform: scale()` | `border-color` (focus transitions only) | `border-color` (continuous keyframe) |
| `transform: rotate()` | `color` (hover transitions only) | `width`, `height` (any animation) |
| `transform: skewX()` | `text-shadow` (title glow only — see exception below) | `clip-path` (any animation) |
| — | — | `left`, `right`, `top`, `bottom` (any animation — use `transform: translateX()` instead) |

#### Exceptions

1. **`text-shadow` in title glow** (§7.1): This is the **only** continuous keyframe animation of a non-GPU property. It is acceptable because:
   - It runs on a single element (`.game-title`) that is rendered once.
   - It creates the pixel-art RPG atmosphere that is central to the brand.
   - It is disabled under `prefers-reduced-motion: reduce`.
   - **Do not add more `text-shadow` keyframe animations.**

2. **Walker horizontal movement** (§7.9): Uses `transform: translateX()` (not `left`/`right`) via a wrapper element pattern. This is the correct GPU-composited approach.

3. **`box-shadow` / `background-color` on hover** (§3.1, §3.2): These are **transitions** between two states, not continuous keyframe animations. Transitions on interaction are allowed and performant for single elements.
### 14.2 will-change

Use `will-change` sparingly — only for elements that animate **continuously on `transform` or `opacity`**:

```css
/* ✅ Correct: continuous transform/opacity animations */
.pixel-sun,
.pixel-cloud-1,
.pixel-cloud-2,
.windmill-blades,
.pixel-walker {
    will-change: transform;
}

.loading-text {
    will-change: opacity;
}

/* ❌ Incorrect: will-change: text-shadow has negligible performance benefit.
   Browsers do not optimize for text-shadow the same way as transform/opacity.
   Remove if found in any codebase. */
```

**Never** use `will-change` on:
- Elements that animate on hover only (buttons, inputs) — triggers unnecessary GPU layer promotion
- Elements that animate once on entrance — no continuous animation to optimize
- More than 10 elements per page — excessive GPU memory usage
- Any property other than `transform` or `opacity` (e.g., `text-shadow`, `background-color`)

> **will-change best practice:** Apply it via JavaScript when the animation starts and remove it when it ends,
> rather than in CSS where it persists for the element's lifetime.

### 14.3 Reduced Paint Area

- Scene animations (clouds, sun, blades, wheat, walkers, sign) run only on `.pixel-scene` which is `position: absolute` and `pointer-events: none` — no layout impact.
- Scanline overlay uses `::before` pseudo-element — no extra DOM node.
- All scene animations use `transform` and `opacity` only (with the single exception of `text-shadow` for the title glow, which runs on one element).

### 14.4 Animation Count Limits

| Context | Max Simultaneous Animations | Example |
|---------|----------------------------|---------|
| Scene (background) | 10 | Clouds, sun, blades, wheat, walkers, sign |
| Interactive (foreground) | 2 | Button hover, input focus |
| Screen transition | 1 | Fade between screens |
| Modal | 2 | Overlay fade + content slide |

### 14.5 Hover Glow Performance

Buttons animate `box-shadow` on hover, which triggers paint. This is acceptable for single buttons but must be constrained:

- **Maximum one glowing hovered button at a time** (natural — only one element can be `:hover`).
- **Hover glow must never be used on repeated lists** (>20 elements, e.g., leaderboard rows, quest lists). For lists, use `background-color` transition only (no `box-shadow`).
- **Do not add `box-shadow` keyframe animations** — hover transitions only.
---

## 15. Animation Token Reference

### 15.1 Duration Tokens (from `design_tokens.json`)

| Token | Value | Category |
|-------|-------|----------|
| `animation.duration.instant` | `0.1s` | Interaction feedback |
| `animation.duration.fast` | `0.3s` | Hover, focus, transitions |
| `animation.duration.normal` | `0.4s` | Walker bob, modal entrance |
| `animation.duration.slow` | `1.5s` | Loading pulse |
| `animation.duration.scene.glow` | `3s` | Title glow, window glow, scanline |
| `animation.duration.scene.sway` | `4s` | Wheat sway |
| `animation.duration.scene.signSway` | `5s` | Wood sign sway |
| `animation.duration.scene.sunPulse` | `6s` | Sun pulse |
| `animation.duration.scene.blades` | `8s` | Windmill blades |
| `animation.duration.scene.walkerFast` | `18s` | Walker 1 |
| `animation.duration.scene.walkerLeft` | `22s` | Walker 3 |
| `animation.duration.scene.walkerSlow` | `24s` | Walker 2 |
| `animation.duration.scene.cloudFast` | `40s` | Cloud 1 drift |
| `animation.duration.scene.cloudSlow` | `55s` | Cloud 2 drift |

> **Token naming convention:** Durations follow a hierarchical `scene.*` pattern for background animations,
> while interaction durations (`instant`, `fast`, `normal`, `slow`) are short names at the top level.

### 15.2 Timing Function Tokens

| Token | Value | Used For |
|-------|-------|----------|
| `animation.timingFunction.linear` | `linear` | Walkers, clouds, blades, scanlines |
| `animation.timingFunction.ease` | `ease` | Default transitions |
| `animation.timingFunction.easeInOut` | `ease-in-out` | Glow, sway, pulse, bob |

### 15.3 Keyframe Index

| Keyframe | File | Line | Used By |
|----------|------|------|---------|
| `pulse-text` | `main.css` | ~135 | `.loading-text` |
| `glow` | `dark-fantasy.css` | ~28 | `.game-screen .game-title` |
| `scan` | `dark-fantasy.css` | ~57 | `.game-screen::before` |
| `sun-pulse` | `pixel-scene.css` | ~49 | `.pixel-sun` |
| `cloud-drift` | `pixel-scene.css` | ~67 | `.pixel-cloud-1`, `.pixel-cloud-2` |
| `blades-spin` | `pixel-scene.css` | ~101 | `.windmill-blades` |
| `window-glow` | `pixel-scene.css` | ~125 | `.house-window` |
| `wheat-sway` | `pixel-scene.css` | ~159 | `.wheat-stalks`, `.wheat-stalks-2` |
| `walker-bob` | `pixel-scene.css` | ~225 | All `.pixel-walker` |
| `walk-right` | `pixel-scene.css` | ~210 | `.walker-1`, `.walker-2` |
| `walk-left` | `pixel-scene.css` | ~215 | `.walker-3` |
| `sign-sway` | `pixel-scene.css` | ~240 | `.sign-hanger` |

### 15.4 CSS Transition Properties

| Selector | Property | Duration | Easing | File |
|----------|----------|----------|--------|------|
| `.btn-primary` | `bg, box-shadow, color, transform` | `0.3s/0.1s` | `ease` | `main.css` |
| `.form-input` | `border-color, box-shadow, bg` | `0.3s` | `ease` | `main.css` |

> **Note:** All transitions use **explicit properties** — never `transition: all`. See §1.2 for the rule.

### 15.5 Complete Animation Map

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          ANIMATION CATEGORIES                                │
├────────────┬──────────┬──────────┬──────────┬───────────┬──────────┬────────┤
│  Hover/    │  Click/  │  Screen  │ Loading  │   Scene   │  Modal   │ Card/  │
│  Focus     │  Active  │  Trans.  │          │ (Backgr.) │          │ Menu   │
├────────────┼──────────┼──────────┼──────────┼───────────┼──────────┼────────┤
│ button-    │ button-  │ screen-  │ loading- │ title-glow│ modal-   │ card-  │
│ hover      │ active   │ switch   │ pulse    │ scanline  │ enter    │ enter  │
│ 0.3s ease  │ 0.1s     │ 0.2s     │ 1.5s     │ 3s        │ 0.2s     │ 0.3s   │
│            │          │ ease     │ ease-    │ linear    │ ease     │ ease   │
│ input-     │ button-  │          │ in-out   │ sun-pulse │ modal-   │ stat-  │
│ focus      │ active   │          │          │ 6s        │ exit     │ stagger│
│ 0.3s ease  │ (wood)   │          │          │ ease-     │ 0.15s    │ 50ms   │
│            │ 0.1s     │          │          │ in-out    │ ease     │ each   │
│            │          │          │          │ cloud-    │          │        │
│            │          │          │          │ drift     │          │ menu-  │
│            │          │          │          │ 40-55s    │          │ item-  │
│            │          │          │          │ linear    │          │ enter  │
│            │          │          │          │ blades    │          │ 0.2s   │
│            │          │          │          │ 8s linear │          │ ease   │
│            │          │          │          │ wheat-    │          │        │
│            │          │          │          │ sway      │          │        │
│            │          │          │          │ 4-5s      │          │        │
│            │          │          │          │ ease-     │          │        │
│            │          │          │          │ in-out    │          │        │
│            │          │          │          │ walkers   │          │        │
│            │          │          │          │ 18-24s    │          │        │
│            │          │          │          │ linear    │          │        │
│            │          │          │          │ sign-sway │          │        │
│            │          │          │          │ 5s        │          │        │
│            │          │          │          │ ease-     │          │        │
│            │          │          │          │ in-out    │          │        │
└────────────┴──────────┴──────────┴──────────┴───────────┴──────────┴────────┘
```

---

## Appendix A: Code Templates

### A.1 New Animation Template

When adding a new animation, use this template:

```css
/* ── [Animation Name] ───────────────────────────────────────────────────
   Description: [What this animation does and why]
   Affects: [CSS selector]
   Duration: [X]s
   Easing: [easing function]
   Property: [animated properties]
   Performance: [GPU/CPU — confirm composited]
   Reduced motion: [how it behaves with prefers-reduced-motion]
   ─────────────────────────────────────────────────────────────────── */

@keyframes animation-name {
    from {
        /* starting state */
    }
    to {
        /* ending state */
    }
}

.selector {
    /* ⚠️ Always include animation-fill-mode: forwards for entrance animations
       to keep the final state visible after the animation ends */
    animation: animation-name Xs easing [infinite] [forwards];
}
```

> **animation-fill-mode rule:**
> - **Entrance animations:** Always use `forwards` so the element stays visible in its final state.
> - **Continuous animations:** `infinite` is sufficient; `forwards` is irrelevant since they never end.
> - **Exit animations:** Use `forwards` to keep the element hidden after disappearance.
> - **Never omit `animation-fill-mode`** — without it, the element resets to its pre-animation state, causing visual flicker.

### A.2 Transition Template

```css
.selector {
    transition: [property] [duration] [easing];
}
```

### A.3 Stagger Template

```css
.items {
    opacity: 0;
    animation: entrance-fade 0.3s ease forwards;
}

.items:nth-child(1) { animation-delay: 0ms; }
.items:nth-child(2) { animation-delay: 50ms; }
.items:nth-child(3) { animation-delay: 100ms; }
.items:nth-child(4) { animation-delay: 150ms; }
.items:nth-child(5) { animation-delay: 200ms; }
```

---

---

## 16. Animation Composition

### 16.1 Multiple Animations on One Element

Some elements need multiple animations running simultaneously on different properties.
The standard pattern uses comma-separated `animation` shorthand:

```css
/* Multiple animations on one element — comma-separated */
.selector {
    animation:
        horizontal-move 18s linear infinite,
        vertical-bob 0.4s ease-in-out infinite;
}
```

**Rules:**

| Rule | Explanation |
|------|-------------|
| **Last = priority for same property** | If two animations target `transform`, the **last one listed** wins for `transform`. Always put the bob/small animation last to overlay it without overwriting the full position. |
| **Separate concerns** | Do not merge horizontal movement and vertical bob into one keyframe — keep them as separate, reusable keyframes. |
| **Max 3 animations per element** | Beyond 3, consider grouping via wrapper elements. |
| **Test in `animation` shorthand only** | Do not use individual `animation-name` + `animation-duration` properties — the shorthand ensures consistent ordering. |

### 16.2 Walker Composition (Example)

The walker character uses two simultaneous animations:

```css
.walker-1 {
    animation:
        walk-right 18s linear infinite,   /* ← horizontal movement (transform: translateX) */
        walker-bob 0.4s ease-in-out infinite;  /* ← vertical bob (transform: translateY) */
}
```

**Why this works:** Both animations target `transform`, but `walker-bob` (listed second) wins for `transform`, while `walk-right`'s `translateX` and `opacity` still apply. The result is a smooth diagonal-like bobbing walk.

---

## 17. Animation Events

### 17.1 CSS Event Lifecycle

| Event | When It Fires | Use Case |
|-------|---------------|----------|
| `transitionstart` | When a transition begins after delay | Analytics, logging |
| `transitionend` | When a transition completes | Remove `loading` class, chain to next state |
| `transitioncancel` | When a transition is interrupted | Cleanup, reset state |
| `animationstart` | When a keyframe animation begins | Trigger sound effects, analytics |
| `animationend` | When a keyframe animation finishes (non-infinite) | Show next screen, remove element |
| `animationcancel` | When an animation is aborted | Reset to default state |

### 17.2 When to Use JavaScript Events

- **Screen transitions:** Listen for `transitionend` on `.screen` to update ARIA attributes.
- **Modal close:** After `transitionend` on exit, set `display: none` and `aria-modal="false"`.
- **Notification toast:** After `animationend`, remove the element from DOM.
- **Loading complete:** After `transitionend` on progress bar, enable the continue button.

### 17.3 When NOT to Use JavaScript Events

- **Scene/background animations** (clouds, wheat, walkers): Continuous infinite — no events needed.
- **Hover/focus transitions:** Browser handles them natively; events add unnecessary complexity.
- **Passive entrance animations:** Use CSS `animation-delay` instead of JavaScript timers.

### 17.4 Event Gotchas

| Gotcha | Solution |
|--------|----------|
| `transitionend` fires once per property | Check `event.propertyName` to filter |
| Events don't fire during `display: none` | Use `visibility: hidden` + `opacity: 0` instead |
| `prefers-reduced-motion: reduce` may prevent events | Always check with `matchMedia('(prefers-reduced-motion: reduce)').matches` in JS |

---

## 18. State Machine

### 18.1 Element States

Each interactive element follows this state lifecycle:

```
        ┌──────────┐
        │  idle    │
        └────┬─────┘
             │
        ┌────▼─────┐
        │  hover   │ ←── focus
        └────┬─────┘
             │
        ┌────▼─────┐
        │  active  │ ←── click/tap
        └────┬─────┘
             │
        ┌────▼─────┐
        │ loading  │ ←── async operation
        └────┬─────┘
             │
        ┌────▼─────┐
        │ disabled │ ←── done / error
        └──────────┘
```

### 18.2 State Transitions

| From → To | Animation | Duration | Notes |
|-----------|-----------|----------|-------|
| `idle → hover` | `bg + box-shadow` transition | 0.3s | Ease |
| `hover → idle` | Reverse transition | 0.3s | Same properties |
| `idle → active` | `transform: scale(0.98)` | 0.1s | Instant press feel |
| `active → idle` | `transform: scale(1)` | 0.1s | Release |
| `idle → loading` | `opacity: 0.6` + `pointer-events: none` | Instant | Static state, no animation |
| `loading → idle` | `opacity: 1` + `pointer-events: auto` | 0.3s | Fade back in |
| `idle → disabled` | `opacity: 0.4` + `cursor: not-allowed` | Instant | No animation |
| `disabled → idle` | `opacity: 1` + `cursor: pointer` | 0.3s | Fade back in |

### 18.3 Unallowed Transitions

| Transition | Why Forbidden | Alternative |
|------------|---------------|-------------|
| `disabled → hover` | Disabled elements must not respond to hover | N/A — disabled is terminal |
| `loading → hover` | Loading state must be non-interactive | N/A — pointer-events disables hover |
| `active → loading` | Must release to idle first | Chain via JS: `activeend` → `idle` → `loading` |

---

## 19. Testing Guidelines

### 19.1 Pre-Submission Checklist

Before committing any animation code, verify:

- [ ] Animation runs at **60 FPS** (check via DevTools Performance tab)
- [ ] Animation does **not trigger Layout or Paint** in DevTools (only Composite)
- [ ] `prefers-reduced-motion: reduce` **completely disables** the animation
- [ ] `animation-fill-mode: forwards` is set for entrance/exit animations
- [ ] `transition` uses **explicit properties** (no `all`)
- [ ] No `will-change` for hover-only or entrance-only animations
- [ ] No `left`/`right`/`top`/`bottom` animation — uses `transform: translate*()`
- [ ] `transform-origin` is set explicitly for rotation animations
- [ ] Works on **mobile viewport** (320px width — iPhone SE)
- [ ] No visual flicker on initial render (no `auto` initial state)

### 19.2 DevTools Performance Recording

1. Open **Chrome DevTools → Performance**.
2. Click **Record** (⚫).
3. Trigger the animation (hover, load, click).
4. Stop recording (⬛).
5. Verify:
   - **Green bars** only (Composite) — no pink (Rendering/Paint) or yellow (Layout) associated with the animation.
   - **FPS** stays at 60 (red bars indicate jank).
   - **GPU memory** does not spike abnormally.

### 19.3 Reduced Motion Testing

```javascript
// In DevTools Console:
// 1. Emulate prefers-reduced-motion
// Go to DevTools → Rendering → Emulate CSS media feature prefers-reduced-motion → reduce

// 2. Or via JS:
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
console.log('Reduced motion enabled:', reducedMotion.matches);
```

### 19.4 Cross-Browser Checks

| Browser | Key Check |
|---------|-----------|
| Chrome | ✅ Performance baseline |
| Firefox | `transform-origin` consistency |
| Safari (iOS) | Mobile tap/hover, 60 FPS on 60Hz display |
| Samsung Internet | Android device testing |
| Telegram in-app browser | Mini App compatibility (WebView) |

---

## 20. Browser Support

### 20.1 Minimum Supported Versions

| Feature | Chrome | Firefox | Safari | Samsung Internet | Telegram WebView |
|---------|--------|---------|--------|------------------|------------------|
| CSS `@keyframes` | 43+ | 16+ | 9+ | 4+ | ✅ (Chrome-based) |
| `transform` | 36+ | 16+ | 9+ | 4+ | ✅ |
| `opacity` | 4+ | 16+ | 4+ | 4+ | ✅ |
| `will-change` | 49+ | 52+ | 15.4+ | 4+ | ✅ |
| `prefers-reduced-motion` | 74+ | 63+ | 15+ | 11+ | ⚠️ Partial |
| CSS `transition` | 26+ | 16+ | 9+ | 4+ | ✅ |

### 20.2 Known Issues

| Issue | Affected Browsers | Mitigation |
|-------|-------------------|------------|
| `will-change` ignored in Samsung Internet 4–5 | Samsung Internet 4.x | Graceful degradation — animations still work, just without GPU hint |
| `prefers-reduced-motion` not supported in Telegram WebView (some versions) | Telegram in-app browser (old) | Use `matchMedia() JS fallback` with manual toggle |
| iOS Safari `transform: translateX()` + percentage values | Safari < 15 | Use pixel values (px) instead of percentages in translateX |
| `transform-origin` defaults differ between browsers | All | Always set explicitly for rotation animations |

---

> **Final rule:** If an animation cannot be tested at 60 FPS with `prefers-reduced-motion` handled,
> it must not be merged into production.  
> AI agents: Before writing any animation code, check:
> 1. `design_tokens.json` → `animation` for duration/timing tokens
> 2. `animations.md` (this file) for approved animation types
> 3. `frontend_rules.md` → `Forbidden UI` section for prohibited animations
>
> All animation durations must come from design tokens. Never invent new durations.
