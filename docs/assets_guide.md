# Assets Guide

> This document describes every asset file in the project and is intended for automatic use by AI models when generating code that references or is inspired by these resources.

---

## Directory Structure Overview

```
assets/                          # Python package
├── __init__.py                  # Module marker; doc: "Game graphic resources (pixel art, etc.)"

asset/                           # Raw image assets (not part of Python package)
└── creting_cha_texture/         # Game texture collection
    ├── background/              # 9 background/scene images (dungeons, castles, landscapes)
    └── character/               # 14 character sprites (heroes, knights, rogues, priests)
```

**Important**: The `assets/` directory is a Python package marker. The actual image files live under `asset/creting_cha_texture/`. When the front-end is built, these files should be moved or symlinked to the front-end's public directory (e.g. `frontend/public/assets/`).

---

## Section 1 — Character Sprites (`asset/creting_cha_texture/character/`)

All character images come from or are inspired by the **Soul Knight** game universe — a pixel-art dungeon-crawler. The dominant style is **pixel art** with transparent backgrounds (RGBA PNG) for easy compositing.

---

### 1.1. `knight-soul-knight-knight.gif`

| Property | Value |
|---|---|
| Format | GIF, animated |
| Dimensions | 200 × 200 px |
| Size | 7.5 KB |
| Mode | P (palette) |
| Average Color | `#170f12` (very dark brown) |
| Dominant Color | `#000000` (black background) |

**Purpose**: Animated pixel-art knight character from Soul Knight. Shows a fully armoured knight with a sword/shield, animated (idle or walk animation frames).

**Where to use in the UI**:
- Player avatar / hero selection screen
- Character portrait in the game dashboard
- Animated loading indicator (the GIF loop adds life to loading states)
- Battle screen player representation

**Colors it defines**:
- Deep dark browns/blacks (`#170f12`, `#000000`) for shadows
- Silver/steel gray for armour plates
- Gold/yellow accents on armour trim
- Red/crimson for cape or plume details

**Artistic style**:
- True pixel art (visible square pixels)
- Limited colour palette (≈ 16–32 colours typical of retro pixel art)
- Clean outlines; characters pop without background thanks to transparency
- Stiff, frame-based animation (3–6 frames looping)

**What can be created following this example**:
- Idle animation sprites for player classes (warrior, knight)
- Equipment icons (sword, shield, helmet)
- Animated loading mascots
- Mini-avatars for party/team UI

---

### 1.2. `07690f45ecf05ed47a0777ae51a6eee2.gif`

| Property | Value |
|---|---|
| Format | GIF, animated |
| Dimensions | 240 × 240 px |
| Size | 22 KB |
| Average Color | `#22171c` |
| Dominant Color | `#000000` |

**Purpose**: Animated pixel-art character — possibly a mage or wizard from Soul Knight. The larger file size (22 KB vs 7.5 KB for the knight) suggests more frames or a larger palette.

**Where to use in the UI**:
- Mage/wizard class selection card
- Animated skill preview
- Spellcasting animation reference
- NPC (non-player character) in dialogues

**Colors it defines**:
- Purple/magenta tones for magical effects
- Deep blue robes
- Glowing cyan or white for spell effects
- Dark outlines for definition

**Artistic style**:
- Same Soul Knight pixel-art lineage as the knight
- More colour variety (magic effects add bright accent colours)
- Larger frame count = smoother animation

**What can be created following this example**:
- Magic effect sprites (fireballs, lightning, shields)
- Staff or wand weapon icons
- Mana / energy bar styling
- Floating particle animations

---

### 1.3. `1OC_JFipbhtxep_bsB01mgoWubFZmYkj0KSOEjp0ozBHVSl-guIFRoS-LczY3ImtiFRHVRf0ppwK5S47kYcjVA.png`

| Property | Value |
|---|---|
| Format | PNG (static) |
| Dimensions | 240 × 240 px |
| Size | 1.5 KB |
| Mode | RGBA |
| Average Color | `#171815` |
| Dominant Color | `#000000` |

**Purpose**: Small, highly compressed static pixel-art character portrait. Very small file size (1.5 KB) suggests simple design with few colours and large transparent areas. Likely a character icon or face portrait.

**Where to use in the UI**:
- Small avatar in player info panel
- Friend list / leaderboard entries
- Chat message author icon
- Notification badges

**Colors it defines**:
- Very dark brown/black base
- Small areas of accent colour (weapon, eyes, emblem)

**Artistic style**:
- Ultra-compact pixel art (tiny sprites)
- High contrast — dark body with bright small details
- Minimalist: every pixel carries meaning

**What can be created following this example**:
- Mini map player markers
- Status effect icons (poison, burn, heal)
- Emoji-style reaction icons for chat
- Compact class badges

---

### 1.4. `hjgCcZhHa50krM5oI6JxzzUg5cV0g5Z81yKak5roriGhZoOOdfsODH6XrVrtPCBRBxcrJhmmfKGvOY-FmgDA0A.png`

| Property | Value |
|---|---|
| Format | PNG (static) |
| Dimensions | 144 × 204 px |
| Size | 1.5 KB |
| Mode | RGBA |
| Average Color | `#514b44` |
| Dominant Color | `#000000` |

**Purpose**: Small character sprite sheet or single character pose — the smallest dimensions among all character assets (144×204). The average colour is notably lighter (`#514b44`) than most others, suggesting a lighter-themed character (perhaps a cleric, paladin, or desert-themed).

**Where to use in the UI**:
- Full-body character preview in class selection
- Character on the game board / grid
- NPC in dialogue boxes
- Equipment preview mannequin

**Colors it defines**:
- Light browns, tans, beiges (`#514b44` average)
- Cream/white for cloth or robes
- Gold trim for holy/light-themed equipment

**Artistic style**:
- Taller aspect ratio (portrait) — suitable for full-body display
- Lighter palette contrasts with most other dark characters
- Clean transparent background for compositing

**What can be created following this example**:
- Cleric / paladin class sprites
- Healing effect animations (golden particles, holy light)
- NPC villagers or quest-givers
- Shopkeeper characters

---

### 1.5. `vzjdym-jkXQqqgc3z5h_QXi5Zo3V4wQv_1TEwOQtBrvC-YLJLXpCFb4e5Slu4YmwuUMMIyUqPshxiRhlMjouxw.png`

| Property | Value |
|---|---|
| Format | PNG (static) |
| Dimensions | 240 × 240 px |
| Size | 1.4 KB |
| Mode | RGBA |
| Average Color | `#221915` |
| Dominant Color | `#000000` |

**Purpose**: A static pixel-art character, very small file (1.4 KB) suggesting a simple sprite. The dark average colour (`#221915`) places it in the dark/stealth character archetype — likely a rogue or assassin.

**Where to use in the UI**:
- Rogue/assassin class avatar
- Enemy NPC (bandit, thief)
- Stealth mode icon/indicator
- Daggers/dual-wield equipment display

**Colors it defines**:
- Dark browns and near-blacks (`#221915`)
- Steel gray for blades
- Red or purple accents for stealth/poison themes

**Artistic style**:
- Minimal pixel detail — compact and efficient
- Dark silhouette with bright eye or weapon accents
- Fits the "shadow/stealth" aesthetic

**What can be created following this example**:
- Stealth ability icons (invisibility, shadow step)
- Poison dagger weapon sprite
- Trap indicator icons
- Night/darkness overlay effects

---

### 1.6. `roguenewpng.png`

| Property | Value |
|---|---|
| Format | PNG (static) |
| Dimensions | 300 × 312 px |
| Size | 18 KB |
| Mode | RGBA |
| Average Color | `#3f3235` |
| Dominant Color | `#000000` |

**Purpose**: Newer/fuller rogue character sprite. Larger dimensions (300×312) and file size (18 KB) suggest more detail and a more refined version of the rogue class. The average colour `#3f3235` is a brownish-purplish dark tone, fitting a rogue/assassin.

**Where to use in the UI**:
- Primary rogue class showcase
- Player avatar with more detail
- Character creation preview
- Inventory screen character model

**Colors it defines**:
- Purple/brown leather tones (`#3f3235`)
- Dark grays for cloth
- Silver for weapon blades
- Red belt/scarf accent

**Artistic style**:
- Higher detail than the 1.4 KB rogue sprite
- More colour variation and shading
- Better proportions — more natural human figure
- Pixel art with soft shading (not dithering)

**What can be created following this example**:
- Detailed class portraits
- Equipment/item icons at higher resolution
- Leather armour icons
- Backpack / inventory bag icons

---

### 1.7. `300px-Marlon.png`

| Property | Value |
|---|---|
| Format | PNG (static) |
| Dimensions | 300 × 358 px |
| Size | 14 KB |
| Mode | RGBA |
| Average Color | `#2b1719` |
| Dominant Color | `#000000` |

**Purpose**: Character sprite named "Marlon" — likely a specific NPC or hero from Soul Knight. The 300×358 size is portrait-oriented. Dark red/brown average colour suggests a warrior with red cape or leather armour.

**Where to use in the UI**:
- Named NPC with a distinct identity
- Quest-giver character portrait
- Hero gallery / collection display
- Lore/story screens

**Colors it defines**:
- Deep crimson/red for cape or tunic
- Brown leather for boots/gloves
- Steel/silver for armour
- Warm skin tone

**Artistic style**:
- Named character with unique design details
- Portrait aspect ratio (slightly taller)
- More detailed than generic class sprites
- Recognisable silhouette

**What can be created following this example**:
- Named NPC avatars with unique colour schemes
- Quest-giver UI elements (exclamation/question marks)
- Dialogue portrait frames
- Character lore cards

---

### 1.8. `226-2261918_priest-from-soul-knight-hd-png-download.png`

| Property | Value |
|---|---|
| Format | PNG (static) |
| Dimensions | 860 × 661 px |
| Size | 9.7 KB |
| Mode | RGBA |
| Average Color | `#c6bfa9` |
| Dominant Color | `#f7f7f7` |

**Purpose**: Priest character from Soul Knight — HD PNG. Notable for being the **lightest** character asset: average colour `#c6bfa9` (beige/cream) with dominant `#f7f7f7` (near-white). This is a high-resolution (860×661) character portrait, not a game sprite.

**Where to use in the UI**:
- Priest/cleric class promotional image
- High-quality character portrait
- Loading screen artwork
- Class selection hero image

**Colors it defines**:
- White/cream robes (`#f7f7f7`, `#c6bfa9`)
- Gold trim and holy symbols
- Warm beige skin tones
- Light blue magical accents

**Artistic style**:
- Semi-pixel or HD pixel art (higher resolution)
- Smooth gradients and anti-aliasing
- Detailed face and fabric folds
- Holy/light magic aesthetic

**What can be created following this example**:
- Healing spell effect backgrounds
- Holy/light UI themes
- Angelic or divine NPC designs
- Shiny gold UI borders and frames

---

### 1.9. `506-5069122_soul-knight-characters-knight-hd-png-download.png`

| Property | Value |
|---|---|
| Format | PNG (static) |
| Dimensions | 860 × 540 px |
| Size | 6.4 KB |
| Mode | RGBA |
| Average Color | `#dcc6b3` |
| Dominant Color | `#f7f7f7` |

**Purpose**: HD group portrait of Soul Knight characters. Shows multiple knights/heroes together. High resolution (860×540), light average colour (`#dcc6b3`). A promotional/illustrative piece.

**Where to use in the UI**:
- Multiplayer team selection screen
- Hero gallery (shows cast of characters)
- App store / promotional screenshots
- "Choose your hero" splash screen

**Colors it defines**:
- Warm beige background tones (`#dcc6b3`)
- Multiple character colour schemes:
  - Blue/silver (knight in armour)
  - Red/gold (paladin type)
  - Green/brown (ranger type)
  - Purple/magenta (mage type)

**Artistic style**:
- Group composition with multiple characters
- Semi-pixel art (HD pixels)
- Each character has a distinct colour identity
- Consistent lighting across the group

**What can be created following this example**:
- Multi-character group screens
- Class selection grid with thumbnails
- Team formation UI
- Colour-coded class differentiation in UI

---

### 1.10. `f146dbd21032f4b.png`

| Property | Value |
|---|---|
| Format | PNG (static) |
| Dimensions | 1200 × 1300 px |
| Size | 9.8 KB |
| Mode | RGBA |
| Average Color | `#210b0d` |
| Dominant Color | `#000000` |

**Purpose**: Very large (1200×1300) but very small file (9.8 KB) — implies large transparent areas with a small, highly detailed character. Very dark average colour (`#210b0d`). Likely a dark/evil character — demon, dark lord, or undead.

**Where to use in the UI**:
- Final boss / end-game enemy
- Dark lord character portrait
- Evil faction emblem
- End-game cutscene

**Colors it defines**:
- Pure black and near-black (`#210b0d`)
- Deep red/crimson for eyes or aura
- Dark purple for shadowy areas
- Bright red/orange for fire effects

**Artistic style**:
- High-resolution pixel art
- Large canvas with centred character
- Dramatic dark theme
- Minimal colour palette (mostly blacks + one accent)

**What can be created following this example**:
- Boss health bar UI
- Dark/evil faction icons
- Status effects: fear, curse, darkness
- Dungeon entrance / portal designs

---

### 1.11. `1691767249_grizly-club-p-kartinki-personazhi-soul-knight-bez-fona-55.png`

| Property | Value |
|---|---|
| Format | PNG (static) |
| Dimensions | 1184 × 1184 px |
| Size | 3.4 KB |
| Mode | P (palette, 4-bit) |
| Average Color | `#322d13` |
| Dominant Color | `#000000` |

**Purpose**: Square (1184×1184) character image with transparent background ("без фона" = without background in Russian). 4-bit palette mode suggests limited colours. Average colour `#322d13` — olive/dark green tones. Likely a ranger, elf, or nature-themed character.

**Where to use in the UI**:
- Ranger/archer class selection
- Elf/nature hero portrait
- Forest-themed UI elements
- Pet/companion character display

**Colors it defines**:
- Olive green / dark green (`#322d13`)
- Brown for leather/wood
- Forest green accents
- Earth tones

**Artistic style**:
- 4-bit colour palette (very retro)
- Square composition (good for icons)
- Clean transparency
- Pixel art with dithering

**What can be created following this example**:
- Forest/nature UI themes
- Bow and arrow weapon icons
- Animal companion sprites
- Leaf/vine decorative elements

---

### 1.12. `images.png`

| Property | Value |
|---|---|
| Format | PNG (static) |
| Dimensions | 447 × 447 px |
| Size | 3.3 KB |
| Mode | P (palette, 8-bit colormap) |
| Average Color | `#c5c0a6` |
| Dominant Color | `#ffffff` |

**Purpose**: Light, neutral-toned square image. Average colour `#c5c0a6` (warm gray/beige) with dominant white. The generic name "images.png" suggests it may be a placeholder or general-purpose icon.

**Where to use in the UI**:
- Placeholder avatar while real image loads
- Default profile picture
- Missing image fallback
- Generic NPC portrait

**Colors it defines**:
- Warm gray / beige (`#c5c0a6`)
- White background (`#ffffff`)
- Light brown outlines

**Artistic style**:
- Neutral, warm tones
- Square format (good for icons)
- Limited palette (colormap mode)

**What can be created following this example**:
- Default/fallback UI elements
- Placeholder skeletons
- Muted neutral backgrounds
- Tooltip or info icon designs

---

### 1.13. `images.jpeg`

| Property | Value |
|---|---|
| Format | JPEG (photographic) |
| Dimensions | 419 × 477 px |
| Size | 16 KB |
| Mode | RGB |
| Average Color | `#ac908a` |
| Dominant Color | `#f7f7f7` |

**Purpose**: A real-life or semi-realistic photographic image, not pixel art. Average colour `#ac908a` (warm rose/brown). The smallest JPEG, likely a photo of a cosplay, real armour, or a concept art reference.

**Where to use in the UI**:
- Reference image for AI generation prompts
- Concept art gallery
- Background for lore screens
- Not for direct use in production UI (JPEG lacks transparency)

**Colors it defines**:
- Warm pink/rose tones (`#ac908a`)
- Light skin tones
- Realistic shading — not pixel art

**Artistic style**:
- Realistic / photographic
- Not pixel art — does not match the game's aesthetic
- Useful as colour reference for realistic materials (metal, fabric, skin)

**What can be created following this example**:
- Colour palette extraction for realistic materials
- Inspiration for non-pixel UI elements (if any)
- Reference for shading and lighting

---

### 1.14. `tom-h-img-20190422-121759.jpg`

| Property | Value |
|---|---|
| Format | JPEG (photographic) |
| Dimensions | 810 × 1080 px |
| Size | 37 KB |
| Mode | RGB |
| Average Color | `#514435` |
| Dominant Color | `#4b4434` |

**Purpose**: A photographic image (dated 2019-04-22, named "tom-h"). The largest character file (37 KB). Dark brown average colour (`#514435`). Likely a photo of a person in medieval/fantasy costume or a cosplay reference.

**Where to use in the UI**:
- Reference image for AI-generated character art
- Real-world colour reference for leather, cloth, armour
- Concept art for character design
- Not for direct UI use (JPEG, no transparency)

**Colors it defines**:
- Dark brown earth tones (`#514435`)
- Leather brown (`#4b4434`)
- Natural fabric colours (wool, linen)

**Artistic style**:
- Real-world photography
- Natural lighting, shadows
- Useful for studying how light falls on armour/clothing
- Reference for pixel-art shading

**What can be created following this example**:
- Realistic leather armour textures for pixel art
- Fabric fold patterns
- Natural lighting colour palettes
- Human proportion references

---

## Section 2 — Background / Scene Images (`asset/creting_cha_texture/background/`)

Background images set the atmosphere: dark dungeons, medieval castles, and fantasy landscapes. The dominant style is **dark fantasy pixel art** with rich atmosphere.

---

### 2.1. `pixel-art-dungeon-scene-glowing-archway-video-game-background-design-atmospheric-medieval-featuring-stone-walls-327520218.webp`

| Property | Value |
|---|---|
| Format | WebP |
| Dimensions | 800 × 449 px |
| Size | 38 KB |
| Mode | RGB |
| Average Color | `#2f303b` |
| Dominant Color | `#141723` |

**Purpose**: Pixel-art dungeon scene with a glowing archway — the most representative background for this project. Shows a stone dungeon corridor with an illuminated archway/portal at the end. The average colour `#2f303b` (dark blue-gray) is atmospheric.

**Where to use in the UI**:
- **Primary game background** — main screen backdrop
- Dungeon exploration screen
- Portal/teleport effect reference
- Level transition screens

**Colors it defines**:
- Dark blue-gray stone (`#2f303b`, `#141723`)
- Glowing cyan/teal for the archway light
- Warm orange for torchlight accents
- Deep shadows at screen edges

**Artistic style**:
- True pixel art (visible square pixels)
- Atmospheric lighting — glowing light source
- Perspective composition (corridor leading to archway)
- Dark fantasy mood

**What can be created following this example**:
- Portal/teleport UI animations
- Torch/fire light effect overlays
- Dungeon room transition animations
- Magical glow shader effects

---

### 2.2. `fond-de-donjon-d-art-pixel-bits-pour-les-jeux-ai-généré-341856981.webp`

| Property | Value |
|---|---|
| Format | WebP |
| Dimensions | 800 × 449 px |
| Size | 46 KB |
| Mode | RGB |
| Average Color | `#303540` |
| Dominant Color | `#020916` |

**Purpose**: AI-generated pixel-art dungeon background ("fond de donjon d'art pixel bits" = pixel art dungeon background in French). Average colour `#303540` (dark gray-blue) with dominant `#020916` (near-black). A dark, moody dungeon scene.

**Where to use in the UI**:
- Dark dungeon backdrop
- Battle arena background
- Underground/cave scene
- Horror-themed encounter background

**Colors it defines**:
- Very dark blue/gray (`#303540`, `#020916`)
- Subtle lighter gray highlights on walls
- Minimal colour variation — pure dungeon atmosphere

**Artistic style**:
- AI-generated pixel art
- Muted, desaturated palette
- Strong atmosphere over detail
- Cave/dungeon geometry

**What can be created following this example**:
- Fog/darkness overlay effects
- Cave wall textures
- Underground map tiles
- Ambient particle effects (dust motes)

---

### 2.3. `7e5adc94-0358-4fc7-bf5e-585a6473290d.webp`

| Property | Value |
|---|---|
| Format | WebP |
| Dimensions | 1950 × 1300 px |
| Size | 144 KB |
| Mode | RGB |
| Average Color | `#1d253a` |
| Dominant Color | `#03040b` |

**Purpose**: Very high-resolution (1950×1300) fantasy landscape. The largest background file (144 KB). Average colour `#1d253a` (deep blue) with dominant `#03040b` (near-black). Likely an outdoor night scene with a castle or mountain silhouette.

**Where to use in the UI**:
- **Main menu / title screen background**
- Overworld / world map backdrop
- Night sky landscape
- Cinematic cutscene background

**Colors it defines**:
- Deep navy blue (`#1d253a`)
- Near-black for silhouettes (`#03040b`)
- Maybe moonlight blue highlights
- Star/sky points of light

**Artistic style**:
- High-resolution panoramic
- Night/evening lighting
- Silhouette-based composition
- Atmospheric, expansive

**What can be created following this example**:
- Night sky with stars parallax effect
- Castle silhouette loading screens
- Moonlight glow filters
- World map UI with dark fantasy aesthetic

---

### 2.4. `hammerwatch-castle-dungeon-j9tnv4oacmi7n9fb.jpg`

| Property | Value |
|---|---|
| Format | JPEG (progressive) |
| Dimensions | 1920 × 1080 px |
| Size | 179 KB |
| Mode | RGB |
| Average Color | `#461f1a` |
| Dominant Color | `#010101` |

**Purpose**: Hammerwatch-inspired castle dungeon screenshot (1920×1080, full HD). The name references "Hammerwatch" — a pixel-art dungeon crawler game. Average colour `#461f1a` (dark crimson/brown) — suggests a red-lit dungeon (lava, torches, or blood theme).

**Where to use in the UI**:
- Hell/lava dungeon background
- Castle throne room scene
- Boss arena backdrop
- Fire/lava-themed level

**Colors it defines**:
- Dark crimson red (`#461f1a`)
- Near-black shadows (`#010101`)
- Orange/red for fire/lava glow
- Dark brown for stone

**Artistic style**:
- Hammerwatch game aesthetic (top-down or side-view dungeon)
- Progressive JPEG for smooth web loading
- Red/orange colour palette dominance
- Dungeon architecture with columns and arches

**What can be created following this example**:
- Lava/fire particle effects
- Red-tinted UI themes for danger zones
- Castle dungeon tile maps
- Burning torch animation sprites

---

### 2.5. `2327eb6b-d3ae-4dd1-9b20-ae7c1f0b8ddb.jpg`

| Property | Value |
|---|---|
| Format | JPEG (progressive) |
| Dimensions | 1536 × 640 px |
| Size | 217 KB |
| Mode | RGB |
| Average Color | `#182e46` |
| Dominant Color | `#080719` |

**Purpose**: Wide-format (1536×640 — ~2.4:1 aspect ratio) landscape with average colour `#182e46` (deep blue/teal) and dominant `#080719` (near-black). This is a wide panoramic — likely a coastal or mountain scene under night/twilight.

**Where to use in the UI**:
- **Panoramic banner** for title/header
- Wide splash screen
- Letterboxed cinematic cutscene
- Horizon/landscape establishing shot

**Colors it defines**:
- Deep teal/blue (`#182e46`)
- Near-black for land silhouettes (`#080719`)
- Subtle lighter teal for sky gradient
- Minimal palette — moody and atmospheric

**Artistic style**:
- Cinematic widescreen composition
- Low-light, moody atmosphere
- Gradient sky with silhouette landscape
- Painted/pixel art hybrid

**What can be created following this example**:
- Cinematic letterbox overlays for cutscenes
- Horizon silhouette parallax backgrounds
- Twilight colour palettes
- Wide loading screen banners

---

### 2.6. `fc9642b02ca644cff040c75cbe24698c.jpg`

| Property | Value |
|---|---|
| Format | JPEG (progressive) |
| Dimensions | 736 × 408 px |
| Size | 43 KB |
| Mode | RGB |
| Average Color | `#524958` |
| Dominant Color | `#3c323d` |

**Purpose**: Progressive JPEG with average colour `#524958` (muted purple/gray) and dominant `#3c323d` (dark purple-gray). This is the **only background with purple/magenta tones** — likely a mystical, magical, or enchanted forest/ruins scene.

**Where to use in the UI**:
- Magical forest / enchanted realm background
- Wizard tower / library scene
- Mystical puzzle area backdrop
- Purple/magenta themed UI section

**Colors it defines**:
- Muted purple-gray (`#524958`)
- Dark purple for shadows (`#3c323d`)
- Magical glow accents (pink, magenta, cyan)
- Mystical atmosphere

**Artistic style**:
- Progressive JPEG (loads in passes)
- Purple/magenta colour harmony
- Mystical, ethereal mood
- Softer and less harsh than dungeon images

**What can be created following this example**:
- Magical aura particle effects (purple/pink)
- Enchanted UI themes
- Portal/magic circle animations
- Mana potion / magic item icon sprites

---

### 2.7. `360_F_1837335892_8eBxVIGQSE37qzKoEVPso6r5UORnehoe.jpg`

| Property | Value |
|---|---|
| Format | JPEG (baseline) |
| Dimensions | 639 × 360 px |
| Size | 70 KB |
| Mode | RGB |
| Average Color | `#212233` |
| Dominant Color | `#05071c` |

**Purpose**: Small (639×360) background with very dark average colour (`#212233` — dark blue-gray) and dominant `#05071c` (near-black). Likely a very dark scene — cave interior, dungeon cell, or night forest. The 300 DPI resolution suggests a stock image.

**Where to use in the UI**:
- Dark cave / underground scene
- Prison / cell backdrop
- Night / darkness encounter background
- Small thumbnail for level selection

**Colors it defines**:
- Very dark blue-gray (`#212233`)
- Near-black shadows (`#05071c`)
- Minimal highlights
- Extremely low-light palette

**Artistic style**:
- Stock image quality
- Very dark composition
- Minimal detail visible — relies on atmosphere
- Good for overlay effects (add torches, glow)

**What can be created following this example**:
- Darkness/fog overlay shaders
- Limited-visibility mechanics (fog of war)
- Torch/light radius effects
- Night-vision / dark-vision filter styles

---

### 2.8. `3e715069c332dc0c61d95cf645b89f77.gif`

| Property | Value |
|---|---|
| Format | GIF, animated |
| Dimensions | 1028 × 824 px |
| Size | 1.2 MB |
| Mode | P (palette) |
| Average Color | `#111311` |
| Dominant Color | `#000000` |

**Purpose**: The **only animated background** and the largest file (1.2 MB). Large format (1028×824). Extremely dark average (`#111311`, almost pure black). Likely an animated scene with subtle motion — flickering torches, moving water, drifting fog, or swaying trees at night.

**Where to use in the UI**:
- **Animated main menu background**
- Animated level backdrop (adds life to the game)
- Cinematic cutscene with motion
- Boss encounter with atmospheric animation

**Colors it defines**:
- Near-black base (`#111311`)
- Subtle animated highlights
- Very dark palette — mostly black
- Animation adds depth and life

**Artistic style**:
- Animated GIF (palette-based, 256 colours max)
- Large canvas for immersive atmosphere
- Subtle animation (not flashy)
- Dark, moody, atmospheric

**What can be created following this example**:
- Animated torch fire sprites (GIF or sprite sheet)
- Ambient fog/particle animation
- Moving water/flowing lava effects
- Flickering light overlays

---

### 2.9. `dark-mysterious-stone-doorway-lit-by-flickering-torches-with-skulls-its-base_1228923-2053.avif`

| Property | Value |
|---|---|
| Format | AVIF (next-gen format) |
| Dimensions | Not read by PIL (format too new) |
| Size | 41 KB |
| Mode | — |

**Purpose**: AVIF-format image — the most modern compression format (smaller than WebP/JPEG). The filename describes the content exactly: a dark mysterious stone doorway lit by flickering torches, with skulls at its base. This is a highly thematic dark fantasy entrance scene.

**Where to use in the UI**:
- Dungeon entrance / level start screen
- Boss door / locked gate backdrop
- Loading screen between levels ("Entering the dungeon...")
- Reward / treasure room entrance

**Colors it defines**:
- Dark stone grays
- Warm orange/yellow torchlight
- Dark brown for wooden door elements
- White/gray for skull details

**Artistic style**:
- AVIF format — best compression, modern browsers
- Detailed gothic/dark fantasy architecture
- Dramatic lighting from torches
- Macabre elements (skulls)

**What can be created following this example**:
- Door/gate opening animations
- Torch bracket UI decoration
- Skull-and-crossbone danger icons
- Gothic archway decorative frames

---

## Section 3 — Artistic Style Summary

### 3.1. Overall Style

| Aspect | Description |
|---|---|
| Genre | Dark fantasy RPG |
| Art type | Pixel art (majority), with some photographic references |
| Colour palette | Dark, moody: blacks, deep blues, crimson reds, muted purples |
| Light sources | Glowing archways, torches, magical portals, moonlight |
| Atmosphere | Dungeon crawling, medieval fantasy, magical, mysterious |

### 3.2. Character Palette (derived from assets)

```
Blacks:        #000000, #010101, #03040b, #05071c, #080719
Dark browns:   #170f12, #171815, #210b0d, #22171c, #221915, #2b1719
Olive/green:   #322d13
Warm browns:   #3f3235, #514435, #514b44, #4b4434
Purple/gray:   #524958, #3c323d
Beige/cream:   #ac908a, #c5c0a6, #c6bfa9, #dcc6b3, #f7f7f7
```

### 3.3. Background Palette (derived from assets)

```
Near-black:    #000000, #010101, #020916, #03040b, #05071c, #080719, #141723
Deep blue:     #182e46, #1d253a, #212233
Gray/blue:     #2f303b, #303540
Red/crimson:   #461f1a
Purple:        #524958, #3c323d
```

### 3.4. File Format Distribution

| Format | Count | Use Case |
|---|---|---|
| PNG | 11 | Character sprites with transparency — primary sprite format |
| JPEG | 4 | Backgrounds, photographic references — no transparency |
| WebP | 3 | Modern compressed backgrounds — best quality/size |
| GIF | 2 | Animated sprites and backgrounds |
| AVIF | 1 | Next-gen background — best compression |

---

## Section 4 — Design Patterns & UI Component Inspiration

### 4.1. New Elements That Can Be Created by Reference

| Asset | Inspires These UI Elements |
|---|---|
| Glowing archway background | Portal effect component, teleport animation, magical glow shader |
| Torch-lit scenes | Flickering light overlay, fire particle system |
| Hammerwatch castle | Stone texture patterns, column/corridor decorative frames |
| Knight sprite | Class selection cards, armour/equipment icons, shield UI |
| Mage animated GIF | Spell effect animations, cast bar styling, mana orb icons |
| Priest HD portrait | Healing aura effects, holy light overlay, divine UI theme |
| Group portrait | Multi-character selection grid, party display, team formation |
| Dark boss character | Boss health bar styling, threat/danger indicators, skull icons |
| Night landscape | Starry sky component, moon phase indicator, night overlay filter |
| Animated GIF background | Parallax background system, ambient particle effects |
| 4-bit ranger | Limited-palette pixel icons, retro UI theme option |
| Wood sign (from CSS) | Scroll/medieval message UI, quest log styling |
| Dungeon doorway AVIF | Door/gate transition animation, skull decorative element |

### 4.2. Recommended Path Mapping

When the front-end is built, assets should be referenced as follows:

```tsx
// ✅ Correct — reference assets from frontend/public/
const ASSET_PATHS = {
  characters: {
    knight:       '/assets/character/knight-soul-knight-knight.gif',
    mage:         '/assets/character/07690f45ecf05ed47a0777ae51a6eee2.gif',
    priest:       '/assets/character/226-2261918_priest-from-soul-knight-hd-png-download.png',
    rogue:        '/assets/character/roguenewpng.png',
    marlon:       '/assets/character/300px-Marlon.png',
    ranger:       '/assets/character/1691767249_grizly-club-p-kartinki-personazhi-soul-knight-bez-fona-55.png',
    darkLord:     '/assets/character/f146dbd21032f4b.png',
    group:        '/assets/character/506-5069122_soul-knight-characters-knight-hd-png-download.png',
  },
  backgrounds: {
    dungeonArch:  '/assets/background/pixel-art-dungeon-scene-glowing-archway-video-game-background-design-atmospheric-medieval-featuring-stone-walls-327520218.webp',
    dungeonAI:    '/assets/background/fond-de-donjon-d-art-pixel-bits-pour-les-jeux-ai-généré-341856981.webp',
    nightCastle:  '/assets/background/7e5adc94-0358-4fc7-bf5e-585a6473290d.webp',
    hammerwatch:  '/assets/background/hammerwatch-castle-dungeon-j9tnv4oacmi7n9fb.jpg',
    panorama:     '/assets/background/2327eb6b-d3ae-4dd1-9b20-ae7c1f0b8ddb.jpg',
    enchanted:    '/assets/background/fc9642b02ca644cff040c75cbe24698c.jpg',
    cave:         '/assets/background/360_F_1837335892_8eBxVIGQSE37qzKoEVPso6r5UORnehoe.jpg',
    animatedBg:   '/assets/background/3e715069c332dc0c61d95cf645b89f77.gif',
    doorway:      '/assets/background/dark-mysterious-stone-doorway-lit-by-flickering-torches-with-skulls-its-base_1228923-2053.avif',
  },
} as const;
```

### 4.3. Image Component Usage Rules

```tsx
// ✅ Correct — use with lazy loading and placeholders
function GameBackground({ src, alt }: { src: string; alt: string }) {
  return (
    <div className="relative w-full h-full bg-tg-bg overflow-hidden">
      <img
        src={src}
        alt={alt}
        className="w-full h-full object-cover opacity-40"
        loading="lazy"
      />
      {/* Gradient overlay for readability */}
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-tg-bg/60 to-tg-bg" />
    </div>
  );
}

// ✅ Correct — character sprite with pixel rendering
function CharacterSprite({ src, className }: { src: string; className?: string }) {
  return (
    <img
      src={src}
      alt="Character"
      className={cn('image-rendering-pixelated', className)}
      style={{ imageRendering: 'pixelated' }}
    />
  );
}
```

---

> **Important**: The AI model must use this guide to understand and correctly reference all project assets.  
> Always use the appropriate image format (PNG for sprites with transparency, WebP/AVIF for backgrounds).  
> Respect the dark fantasy pixel-art aesthetic when generating new UI components.
