# לאן? — redlines (senior design review, 2026-11-23)

Refines `spec-polish.md` and does not override it, except in the four places marked **[refines polish]**, each with its reason.
Read with `laan-prompt.md` §0 and §3. Where they conflict, §3 wins: weight ≥ 500, text ≥ 32 (28 allowed only for micro-labels), buttons ≥ 72, contrast ≥ 7:1.

**Evidence base.** The 13 screenshots in `/Users/26yos/at/laan-shots/` were taken at 19:31, before the polish pass.
`index.html` changed at 19:43, so I re-shot all 19 screens from the live build at 412×915 and 360×780 (headless Chrome, `?screen=<id>`):
`/private/tmp/claude-501/-Users-26yos--claude-spares-spare-Sb6iyp/1eecaef2-8ea8-42bd-a785-c960f3993424/scratchpad/cur/` (`<id>.png`, `s-<id>.png`, sheets `A–D.png`, `S1–S2.png`).
The current build already fixes the outlined buttons, the mixed footer tiles, the Secular-One-everywhere type and the filler circles.
Every defect listed below is still visible in the **current** build unless it is marked *(19:31 only)*.

Class names refer to the current `index.html` (`.say .sub .step .card .band .plate .fig .b-pri .b-sec .tile .mic .field .map .alert`).

---

## 1. Tokens (final)

### 1.1 Color — light (default)

| token | hex | used for | measured contrast |
|---|---|---|---|
| `--ground` | `#F7F3EC` | page | — |
| `--surface` | `#FFFFFF` | cards, tiles, field | — |
| `--surface2` | `#EFE7D8` | secondary button, footer bar, strip "next" disc | — |
| `--press` | `#E3D8C3` | pressed fill of secondary / tile / option, strip "done" disc | ink on it **12.56** |
| `--ink` | `#1A1814` | all primary text and icons | ground **16.03** · surface **17.73** · surface2 **14.43** |
| `--ink2` | `#4A443B` | supporting text, micro-labels | ground **8.70** · surface **9.63** · surface2 **7.84** · ✗ on band yellow 6.73 · ✗ on press 6.82 (never use on those) |
| `--placeholder` | `#5A534A` | field placeholder (on surface only) | surface **7.58** |
| `--act` | `#0B3D91` | primary fill, icons in cards, focus ring | white on it **10.04** · as text/icon on ground **9.08**, surface **10.04**, surface2 **8.18** |
| `--act-edge` | `#072A66` | 4px bottom edge of primary | white on it 13.71 (decorative) |
| `--on-act` | `#FFFFFF` | text on primary / yes / no | see fills |
| `--yes` | `#12602F` | yes button | white **7.66** (the prompt's `#1B7F3B` measures 5.07 and fails, so do not revert to it) |
| `--yes-edge` | `#0A4320` | yes edge | — |
| `--no` | `#B00020` | no button | white **7.33** |
| `--no-edge` | `#74000F` | no edge | — |
| `--band` | `#FFD400` | sign band, alert | ink **12.38** · black **14.67** · act **7.02** |
| `--plate` / `--plate-ink` | `#FFFFFF` / `#1A1814` | line-number plate | **17.73** |
| `--amber` | `#FFE7A3` | "איפה אני?" icon disc | ink glyph **14.53** |
| `--amber-edge` | **`#A86F00`** (was `#D99A00`) | 4px top edge of the "איפה אני?" tile | non-text vs surface **4.25**, vs bar **3.46** (`#D99A00` measured 2.45 and failed 3:1) |
| `--ring` | `#C3D2EC` | 4px halo around the strip "current" disc | decorative; act disc vs ground 9.08 carries the meaning |
| `--focus` | `#0B3D91` | 4px focus outline, offset 2px | vs ground **9.08** |

### 1.2 Color — dark (`prefers-color-scheme: dark`, or setting "כהה")

Dark mode inverts the action fills to light tints with dark text, because a deep-blue fill on near-black has no edge.

| token | hex | measured |
|---|---|---|
| `--ground` | `#14120F` | — |
| `--surface` | `#211D18` | — |
| `--surface2` | `#2A251E` | — |
| `--press` | `#3A332A` | ink on it **10.87** · ink2 **7.36** |
| `--ink` | `#F4EFE6` | ground **16.33** · surface **14.63** · surface2 **13.27** |
| `--ink2` | `#CFC6B8` | ground **11.06** · surface **9.91** · surface2 **8.99** |
| `--act` / `--on-act` | `#A8C7FF` / `#0B1A33` | **10.15** · act as text on ground **10.93**, on surface2 **8.89** |
| `--yes` / `--on-yes` | `#8AD5A0` / `#08240F` | **9.54** |
| `--no` / `--on-no` | `#FFA8A8` / `#3A0008` | **9.65** |
| `--band`, `--plate` | unchanged `#FFD400`, `#FFFFFF` + `#1A1814` | band vs ground 13.06 |
| `--amber-edge` | `#E0A82E` | vs surface **7.83** |
| `--focus` | `#A8C7FF` | vs ground **10.93** |
| `--lift` | `none`; cards get `box-shadow: inset 0 0 0 1px #3A332A` instead | — |
| map tiles | `.leaflet-tile-pane{ filter: invert(.9) hue-rotate(180deg) saturate(.3) brightness(.9) }` | — |

High-contrast "שחור־צהוב" stays as it is in code: `#FFE14D` on `#000000` measures **16.13** both ways, and every surface gets the 3px ink outline.

### 1.3 Type

Two families only: **Rubik** (400 is not used, so load 500/700/800) and **Secular One** for the plate and big figures only.
Hebrew gets no letter-spacing (tracking breaks the joins of ש/ם shapes visually), so `letter-spacing: 0` everywhere except the figures.
Use `font-variant-numeric: tabular-nums` on all digits so the countdown does not jitter.

| role | family | weight | size / line-height | tracking | color | class |
|---|---|---|---|---|---|---|
| plate (line number) | Secular One | 400 | 120 / 1.0 (96 at ≤ 860px tall) | -0.02em | plate-ink | `.plate` |
| figure, hero | Secular One | 400 | 96 / 1.0 (80 compact) | -0.02em | ink | `.fig .num` |
| figure, secondary **[refines polish]** | Secular One | 400 | **72** / 1.0 (64 compact) | -0.02em | ink | `.fig.sec .num` |
| figure, inline (distance) | Rubik | 800 | 48 / 1.1 (44 compact) | 0 | ink | `.fig.md .num` |
| alert title | Rubik | 800 | 56 / 1.2 | 0 | currentColor | `.alert .big` |
| title (one-word sentences: "הגעת!") | Rubik | 700 | 48 / 1.25 (44 compact) | 0 | ink | `.say.big` |
| sentence | Rubik | 700 | 40 / 1.3 (1.25 compact) | 0 | ink | `.say` |
| card name, hero | Rubik | 700 | 40 / 1.25 (36 → 32 compact) | 0 | ink | `.card.hero .nm` |
| card name | Rubik | 700 | 32 / 1.25 | 0 | ink | `.card .nm` |
| body / supporting | Rubik | **500** (now 400) | 32 / 1.3 | 0 | ink2 | `.sub .card .ds .fig .soft .fig .unit` |
| button label | Rubik | 700 | 32 / 1.2 | 0 | per button | `button` |
| field text | Rubik | 500 | 36 / 1.2 | 0 | ink | `.field` |
| footer tile label | Rubik | 500 | 30 / 1.1 | 0 | ink | `.tile` |
| quiet button | Rubik | 500 | 30 / 1.2, underline 2px, offset 7px | 0 | ink | `.b-quiet` |
| micro-label (eyebrow, schedule note) | Rubik | 500 | 28 / 1.25 | 0 | ink2 | `.step .figcap` |
| map label | Rubik | 700 | **32** / 1.2 (now 30, which is not an allowed size) | 0 | `#1A1814` on white | `.lbl` |
| demo badge | Rubik | 500 | 24 / 1.0 (demo only, not product) | 0 | ink2 on surface2 | `.badge` |

Wrapping rules, applied globally:
- `.say, .sub, .card .nm` get `text-wrap: balance`. A sentence may run at most 2 lines at 412 and 3 at 360. If it runs longer, the copy is too long.
- Proper names and number+unit pairs never break. Wrap each part in `<span class="nb">` (`white-space: nowrap`): "דיזנגוף", "/", "קינג ג'ורג'", "18 דקות", "כ־25 מטר".
- Set `overflow-wrap: normal` on names (`.card .nm, .lbl, .band .dir, .alert .where`). The global `overflow-wrap: break-word` is what splits "ז'בוטינ|סקי" at 360.
- Use U+2011 (non-breaking hyphen) or a nowrap span inside compounds with a maqaf: "סופר־פארם" must not break at the maqaf.
- The stop-name separator is `" / "`: a thin space U+2009, the slash, then a thin space. It is a break opportunity only between the parts.

### 1.4 Spacing

Base scale: **8 · 16 · 24 · 32 · 48**. Compact mode (≤ 800px tall) maps 24→12 and 16→12. That compact mapping is the only place 12 appears.

| use | 412×915 | ≤ 860 tall | ≤ 800 tall |
|---|---|---|---|
| screen side padding | 20 (+ safe-area) | 20 | 20 |
| between layout bands (`--gap`) | 24 | 16 | 12 |
| eyebrow → sentence | 8 | 8 | 4 |
| sentence → sub | 8 | 8 | 4 |
| between stacked buttons | 16 | 16 | 12 |
| inside cards | 20 inline / 16 block | 16 / 12 | 16 / 10 |
| footer bar padding | 12 block, 20 inline | 12 | 10 top / 12 bottom |
| footer tile gap | **16** (now 12) | 16 | 12 |
| icon ↔ label in buttons | **12** (now 16) | 12 | 12 |

### 1.5 Radii (by role)

| radius | role |
|---|---|
| 8 | demo badge, map labels (now 10) |
| 12 | sign plate, landmark icon tile |
| 16 | **all buttons** (now 18), field, footer tiles, mic in row |
| 20 | cards, band, map panel, list, alert button |
| 50% | discs: strip nodes, mic (round), okdisc, amber disc |

The plate sits inside the band: band radius 20, band padding 16 → plate radius 12, so the nested curves stay concentric.

### 1.6 Elevation

| level | value | used on |
|---|---|---|
| e0 | none | everything by default: buttons, tiles, band, plate |
| e1 | `0 1px 2px rgba(26,24,20,.08), 0 8px 24px rgba(26,24,20,.06)` | cards, list, map panel, shortcut rows, field |
| e2 | `0 1px 2px rgba(26,24,20,.25), 0 4px 12px rgba(26,24,20,.18)` | map labels and markers only |
| tactile edge | `inset 0 -4px 0 var(--edge)` → `inset 0 -1px 0` pressed | primary, yes, no, mic |

Dark mode: e1 becomes `inset 0 0 0 1px #3A332A`, and e2 stays (it sits on the map).

### 1.7 Icons

24 viewBox, stroke 2.5, round caps and joins, `currentColor`. Stroke 2 at ≥ 96px.

| size | where |
|---|---|
| 22 | glyph inside a 36px strip disc |
| 28 | glyph inside the 40px amber disc |
| 32 | footer tile icon, quiet button |
| 36 | button icons, list rows |
| 44 | card icon, mic in circle |
| 36 in a 56×56 tile | landmark card (radius 12, surface2) |
| 120 | alert bus |

Only direction icons (arrow, chevron) mirror in RTL. The walk icon faces the direction of travel, so it does not mirror.
Do not use a **clock** for "recent" (older readers read it as "schedule / late"). Use a pin for places and a home for home.

### 1.8 Motion

| motion | duration / easing | reduced-motion |
|---|---|---|
| screen change | **none** (instant swap; focus moves to `.say`) | same |
| button press | instant state change, no transition | same |
| mic listening pulse | 2000ms `ease-in-out` infinite, halo 0 → 22px, `rgba(11,61,145,.45)` → 0 | static 8px `--ring` halo |
| planning progress bar | width 8000ms `linear` | width jumps at each real step (25/50/75/100%) |
| alert flash | 1000ms `steps(1,end)` (1 Hz) | 2000ms (0.5 Hz), never off: it is a safety signal |
| countdown digit change | none | none |

---

## 2. Components

### 2.1 Top row (56px; 48 at ≤ 860 tall)

- Layout: `display:flex; align-items:center; gap:12px`. The strip or section label sits at inline-start, and the inline-end side stays **empty**.
- **Journey strip** (walk → stop → ride → arrive), 4 discs and 3 connectors:

| state | disc | glyph | extra |
|---|---|---|---|
| done | 36px, `--press` `#E3D8C3` (now ink-black) | check, 22px, ink | — |
| current | 36px, `--act` | step icon, 22px, white | 4px `--ring` halo |
| next | 36px, `--surface2` | step icon, 22px, ink2 | — |
| connector | 24 × 3px, radius 2, margin-inline 4 | — | done side `--ink2`, next side `--surface2` |

  **Why:** four black discs on the arrived screen are the heaviest thing on screen. Done steps should recede, not shout.
  The strip is `role="img"` with `aria-label="שלב 2 מתוך 4: בתחנה"`. The eyebrow line under it is its visible text label (2.2).
- **Section label** on non-journey screens is 28/500 ink2: "היכרות · 1 מתוך 5", "תכנון הדרך", "איפה אני?", "עזרה", "הגדרות".
  Onboarding adds 16px dots, with the current one 24px blue plus halo.
- **Wordmark** ("לאן?" plate on yellow, 32px Secular One) appears on welcome and dest-first/dest-return only. Remove it from confirm, planning, nodirect, lost and help.
- **Demo badge** **[refines polish]**: polish asked to move it to "bottom-start above the footer", but there is no free band there. Make it a tab sitting on the footer bar's top edge instead:
  `position:absolute; top:-14px; inset-inline-end:20px; height:26px; padding:0 8px; font:500 24px/26px Rubik; radius 8px 8px 0 0; background:var(--surface2)`.
  At ≤ 800 tall: `top:-11px; height:22px; line-height:22px`. It never sits in the top row.

### 2.2 Sentence block

- An optional **eyebrow** (28/500 ink2, 1 line, `text-overflow: clip` never ellipsis) states the current step in words. It is the strip's text label.
  walk "בדרך לתחנה" · stop "בתחנה דיזנגוף / קינג ג'ורג'" · ride "קו 5 לכיוון רידינג" · finalwalk "בדרך למרפאה" (short name, ≤ 18 chars, so it never wraps at 360).
- **Sentence** `.say` 40/700, ≤ 12 words, ≤ 2 lines at 412. `tabindex=-1` gets focus on screen entry.
- **Sub** `.sub` 32/**500** ink2, ≤ 1 line at 412 when there is a hero below, ≤ 2 when there is not.
- The block is pinned to the same y on every screen (see §3 grid). It is never vertically centered.

### 2.3 Sign band + plate (stop screen; welcome wordmark variant)

- **Band**: `--band`, radius 20, padding 16 block / 20 inline, column, `align-items:center`, gap 8. Width 100%.
- **Plate**: Secular One 120/1.0, `min-width:1.4em`, padding **16px 32px 8px** (Secular digits sit high, so the bottom padding is less), border **4px** `--plate-ink`, radius 12, `--plate` fill.
  The plate is the only outlined element in the app.
- **Direction** under the plate: "לכיוון רידינג" 32/700 band-ink, **one line**, nowrap per part. If the headsign is longer than 14 chars, drop to 28/700. Never use 2 lines.
- The stop name **does not** go in the band (polish rule). It goes in the eyebrow.
- Compact (≤ 860 tall): band switches to row (`.band:not(.solo)`), plate 96 at inline-start, direction at inline-end in **2 fixed lines**: "לכיוון" (28/500) above "רידינג" (32/700). This replaces today's ragged wrap.
- **The plate is reserved for line numbers.** **[refines polish]** Counts (stops left) use the figure (2.4), never the plate, because a "3" in a bus-sign plate reads as "line 3".

### 2.4 Figure (countdown / count / distance)

- Structure: `[prefix] [num] [unit]` on one baseline, `column-gap:12px`, centered. RTL order is "בעוד 5 דקות".
- Hero figure is used when nothing else on the screen is bigger (ride): num 96 Secular One, prefix/unit 32/700 ink.
- Secondary figure is used **when a plate is on screen** (stop): num **72**, prefix/unit 32/700. **[refines polish: 96 → 72]**
  **Why:** in the demo the plate "5" (120px) and the countdown "5" (96px) are two giant identical digits stacked 60px apart, and the eye cannot tell which is the line number.
- Inline distance figure (walk / finalwalk): num 48 Rubik 800 + unit 32/700, then on the **same row** at inline-end, separated by 24px, the soft part "כ־4 דקות" 32/500 ink2. This takes one row instead of today's two.
- Caption `.figcap` 28/500 ink2, centered, 8px under, e.g. "לפי לוח הזמנים". No parentheses.

### 2.5 Map panel

- Panel: radius 20, e1, `--surface2` fill while loading. Height comes from flex with **min 42% of viewport on walk/finalwalk** (≈ 384px at 915; min 200 at 780).
- Tiles: `.leaflet-tile-pane{ filter: saturate(.35) contrast(.95) brightness(1.04) }`. Full-color OSM POI icons (purple carts, stars of David, cinema icons) out-shout the route.
- Route: **8px** `#0B3D91`, round caps, on a **12px white casing** (two polylines). Dash nothing.
- "You": 30px `#0B3D91` disc, 5px white border, 3px blue outer ring (46 total), e2. Label below at 24px gap.
- Target: 40px pin head `#B00020`, 5px white border, e2. Label above at 60px.
- **Labels: short generic words at 32/700**, white chip, radius 8, padding 2px 12px, e2: "אתה"/"את", "התחנה", "המרפאה" (short destination kind).
  The full name lives in the sentence/eyebrow. **Why:** "דיזנגוף / קינג ג'ורג'" at 32px is ~330px and clips at the map edge (finalwalk "רפאת כללית" is cut at 360 today).
- Keep every label inside the panel: compute the chip's bounds after `fitBounds` and flip it to the other side of the marker if it would clip. `fitBounds` padding is 64px top, 48 sides, 48 bottom.
- Attribution: 11px at the bottom-end corner, `background: rgba(255,255,255,.8)`, never over a marker. It is legal text, so the size exception applies.

### 2.6 Card (generic) and landmark card

- Card: surface, radius 20, e1, padding 16 / 20, row, gap 16, `align-items:center`.
  Icon 44 `--act`. Name 32/700 (hero 40/700). Desc 32/**500** ink2, gap 4.
- Non-interactive cards never carry an icon that looks tappable. A **phone icon on the contact card is wrong** (help, 19:31 and current), so use a 56px initial disc instead ("ר" 32/700 on surface2).
- No "·" middots inside desc lines: "בית מרקחת • כ־25" wrapped with the bullet at a line start at 360. Use a comma: "בית מרקחת, כ־25 מטר ממך".
- **Landmark card** (lost-landmark): a 56×56 icon tile (radius 12, surface2) with a 36px kind icon (pharmacy cross / bank / cart / tree) at inline-start.
  Name 40/700 hero, nowrap per word, 2 lines max. Desc 32/500: kind + distance.

### 2.7 Summary list (sent)

- List: surface, radius 20, e1, padding 8 / 20. Rows: min-height 64, padding-block 12, gap 16, icon 36 `--act`, text 32/500 ink.
- Divider: `box-shadow: 0 -2px 0 var(--surface2)` (as now), inset to start at the text, not under the icon: `margin-inline-start: 52px` on the divider pseudo.
- Exactly 3 rows, each **one line at 412** (≤ 18 chars): see §3 sent.

### 2.8 Buttons

| type | height (412 / ≤860 / ≤800) | fill / text | edge | radius | pressed | label max |
|---|---|---|---|---|---|---|
| primary `.b-pri` | 92 / 80 / 80 | act / on-act 32/700 | 4px act-edge | 16 | edge → 1px, content +3px down (`padding-block: 11px 9px`) | 16 chars with icon at 412, **14 at 360** |
| yes `.b-yes` / no `.b-no` | same as primary | yes or no / white | 4px yes/no-edge | 16 | same | same |
| secondary `.b-sec` | 76 / 72 / 72 | surface2 / ink 32/700 | none | 16 | fill → `--press` | 16 / 14 |
| quiet `.b-quiet` | 72 | transparent / ink 30/500, underline 2px offset 7px | none | 16 | fill → `--surface2` | — |
| option `.opt` (settings) | 92 / 80 / 80 | surface2 / ink; selected = act + check icon 36, `aria-pressed=true` | none (selected: 4px act-edge) | 16 | fill → `--press` | 8 |

- Padding is 0 20px. Icon 36 at inline-start, gap 12. Content is centered.
- **Labels never wrap.** If the label does not fit at 360, shorten the copy (§3). Never shrink the type below 32.
- Focus: `:focus-visible{ outline:4px solid var(--focus); outline-offset:2px }`. Programmatic focus (screen entry) shows no ring.
- Disabled: never used. Debounce of 600ms is silent (no visual change).
- Order: primary on top, secondary under. In a yes/no pair, yes is on top. Max 2 buttons in `.actions`.
- **Color semantics** **[refines polish]**: green/red pairs are used only when "no" means *that fact is wrong* (confirm, landmark, resume).
  When the "no" answer is the calm one ("אני בסדר"), use primary + secondary (offroute). A lone confirmation (off) is a primary, never a single green button.

### 2.9 Footer bar + tiles

- Bar: surface2, full-bleed, padding 12 20 (12 + safe-area bottom). No top rule (hc mode: 3px ink top rule).
- Two equal tiles: `flex:1 1 0`, gap **16**, min-height 88, radius 16, surface, column, gap 4, padding 8 6.
  Icon 32 above label 30/500 ink, nowrap.
- "לשמוע שוב" (inline-start): speaker icon 32 ink.
- "איפה אני?" (inline-end): 40px amber disc with a 28px compass glyph, plus `box-shadow: inset 0 4px 0 #A86F00`.
- Pressed: fill → `--press`.
- In the help flow (lost-*, help, sent, offroute) "איפה אני?" is hidden. The single tile keeps **half width at inline-start** (now it stretches full width), so "לשמוע שוב" never moves under the thumb.
  The other half is empty bar.

### 2.10 Input field + mic

- Field: height 76 standalone / 88 in a row, radius 16, surface, e1 + `inset 0 0 0 2px var(--surface2)`, padding-inline 20, Rubik 500 36, `dir="auto"`.
  Placeholder `#5A534A` ("או לכתוב כאן" / "לכתוב כאן"). Focus: 4px focus outline offset 2. When focused, `scrollIntoView({block:'center'})`.
- Mic, round (dest-first, lost-ask): `min(160px, 20dvh)`, act, edge 4px, icon 44 above label "לדבר" 32/700.
- Mic, row variant (dest-return): 104 × 88, radius 16, icon 36 above label.

| state | mic | sentence / label | field |
|---|---|---|---|
| idle | act fill, label "לדבר" | screen sentence | placeholder |
| listening | same fill, pulse halo 2s; label "מקשיב..." | sentence becomes "אני מקשיב..." | read-only, placeholder hidden |
| processing (≤ 8s) | fill stays, icon swaps to a static 3-dot glyph (no spinner); label "בודק..." | "רגע, אני בודק..." | shows the transcript in ink |
| error | back to idle | "לא שמעתי. אפשר לנסות שוב או לכתוב." | focus moves to field |

### 2.11 Alert overlay

- Fixed, inset 0, z 1000. Column, centered, gap **32**. Padding 24 20 + safe areas. Flash between `#FFD400`/`#000` and `#000`/`#FFD400`, 1 Hz steps.
- Bus icon 120, stroke 2.
- Title 56/800 lh 1.2, **forced break** "יורדים<br>בתחנה הבאה!". Today "בתחנה" sits alone on line 1.
- Stop name 40/700 (clamp 32–40), **no quotation marks**, nowrap per part.
- Button "הבנתי": min-height 120, radius 20, border 4px currentColor, 48/800, width 100%, inverse flash.
- **No blue focus ring** on the auto-focused button (current screenshot shows `#0B3D91` around it). If it gets keyboard focus: `outline: 6px solid currentColor; outline-offset: 4px`.
- After "הבנתי": static `#000` on `#FFD400` (`.still`).

---

## 3. Per screen

### 3.0 The shared grid (every screen)

| band | 412×915 | 360×780 |
|---|---|---|
| top pad | 0–8 | 0–8 |
| top row | 8–64 | 8–56 |
| eyebrow (optional) | 88–123 | 68–103 |
| sentence start | 131 with eyebrow / 88 without | 107 / 68 |
| sentence line | 52px | 50px |
| hero | sentence-end + 24 → actions-top − 24, content centered (map: fills) | +12 / −12 |
| actions, 1 button | 687–779 | 578–658 |
| actions, primary + secondary | 595–687 · 703–779 | 494–574 · 586–658 |
| actions, yes/no | 579–671 · 687–779 | 486–566 · 578–658 |
| footer bar | 803–915 (tiles 815–903) | 670–780 (tiles 680–768) |

Copy rule: masculine / feminine pairs are written **m / f**. Where Hebrew allows it, use impersonal plural or infinitive ("עולים", "יורדים", "לחזור"), which avoids a fork.

### 3.1 welcome
- **Hero:** the wordmark band ("לאן?" + "הוראה אחת בכל פעם").
- **412:** top dots + "היכרות · 1 מתוך 5" · sentence 88–192 (2 lines) · band centered in 216–663 (≈ 330–550) · primary 687–779 "בואו נתחיל" · footer.
- **360:** band 260–488. Tagline breaks as "הוראה אחת בכל / פעם" (widow).
- **Fixes:** (1) Tagline: `text-wrap:balance` and nowrap "בכל פעם", which gives "הוראה אחת / בכל פעם". (2) The section label lost the count, so restore "1 מתוך 5" after "היכרות". (3) No other change.
- **Copy:** unchanged ("שלום! אני אעזור לך להגיע בקלות." is gender-neutral in writing).

### 3.2 dest-return
- **Hero:** the shortcuts (one tap = done).
- **412:** wordmark + "תכנון הדרך" · sentence 88–140 "שלום שוב! לאן היום?" · shortcuts **top-aligned** from 164: rows 88 tall, gap 16 → 164–252, 268–356, 372–460 · input row 484–572 (mic 104×88 at inline-start, field fills) · no actions · footer · quiet "הגדרות" under the footer (72).
- **360:** rows 68–… with gap 12. Every shortcut must stay 1 line.
- **Fixes:** (1) There is a dead 100px void between sentence and first row, because the list is vertically centered. Use `.mid.top`. (2) Clock icons → pin icon (home keeps home). (3) "מרפאת כללית, דיזנגוף" and "קניון דיזנגוף סנטר" wrap at 360, giving rows 76 vs 104 tall. Store a **short name ≤ 14 chars** for shortcuts ("כללית דיזנגוף", "דיזנגוף סנטר") and keep the full name for confirm.
- **Copy:** unchanged.

### 3.3 confirm
- **Hero:** the place card (name 40/700 + distance).
- **412:** "תכנון הדרך" · sentence 88–140 **"זה המקום?"** · card centered in 164–555 · yes 579–671 "כן" ✓ · no 687–779 "לא" ✗ · footer.
- **360:** card 2 lines name + 1 line distance.
- **Fixes:** (1) The sentence and the card both say "מרפאת כללית, דיזנגוף", so the name is printed twice. The sentence asks and the card states. Voice still reads "מרפאת כללית, דיזנגוף. זה המקום?". (2) "ק״מ" is an abbreviation (§0.5): write "כ־1.5 קילומטר מכאן", rounded to 0.5 km above 1 km. (3) "1.6 ק״מ / מכאן." wraps at 360. Nowrap "כ־1.5 קילומטר".
- **Copy:** "זה המקום?" (neutral) · desc "כ־1.5 קילומטר מכאן".

### 3.4 planning
- **Hero:** the progress bar, placed close to the sentence.
- **412:** "תכנון הדרך" · sentence 88–192 "רגע, אני מחפש לך אוטובוס..." · sub 200–242 "רק אוטובוס ישיר, בלי החלפות." · bar at 290–306 · caption 322–364 "זה לוקח כמה שניות." (32/500 ink2) · no actions · footer.
- **360:** same order, bar at 260.
- **Fixes:** (1) The bar floats alone at y≈540 in a 470px void. Pin it 48px under the sub. (2) The bar is 24px tall and its 4% fill reads as a toggle knob. Make it 16px tall, radius 8, and set the fill `min-width:16px` with a start of 10%. (3) Sub is 2 lines at 412. `text-wrap:balance` makes it one line at 412 ("רק אוטובוס ישיר, בלי החלפות.").
- **Copy:** add the caption. Everything else unchanged.

### 3.5 walk
- **Hero:** distance "250 מטר" with the map as its picture.
- **412:** strip · eyebrow 88–123 "בדרך לתחנה" · sentence 131–235 m "לך לתחנה דיזנגוף / קינג ג'ורג'." / f "לכי לתחנה …" · figure row 259–312 "250 מטר  כ־4 דקות" · map 336–663 (≥ 42%: drop the eyebrow when the sentence needs 2 lines; then map 293–663 = 370px) · primary 687–779 "יצאתי לדרך" · footer.
- **360:** sentence 3 lines max, map min 200.
- **Fixes:** (1) The quotation marks around the stop name, plus the trailing `".`, add three marks of noise, and at 360 the name breaks "קינג / ג'ורג'". Remove the quotes and nowrap the parts. (2) Figure + soft line take 2 rows (95px). One row (53px) gives the map back 42px. (3) Map: desaturate tiles, use generic labels "התחנה"/"אתה", and give the route its casing. Today the route is nearly invisible under the POI icons.
- **Copy:** m "לך לתחנה דיזנגוף / קינג ג'ורג'." f "לכי לתחנה דיזנגוף / קינג ג'ורג'."

### 3.6 stop
- **Hero:** the plate "5".
- **412:** strip · eyebrow 88–123 "בתחנה דיזנגוף / קינג ג'ורג'" · sentence 131–183 "עולים על קו 5" · band 207–419 (plate 120 + direction 1 line) · figure (secondary, 72) 443–515 "בעוד 5 דקות" · figcap 523–558 "לפי לוח הזמנים" · primary 595–687 · secondary 703–779 · footer.
- **360:** band in row mode 159–301 (plate 96, "לכיוון / רידינג" fixed 2 lines) · figure 64.
- **Fixes:** (1) Two near-equal giant "5"s. Countdown digits go to 72 (2.4). (2) At 360 both buttons wrap to 2 lines ("עליתי על / האוטובוס", "האוטובוס / לא מגיע?"). Shorten the copy. (3) Sentence "עלה על קו 5" is gendered and restates the plate. "עולים על קו 5" is neutral and pairs with the alert's "יורדים".
- **Copy:** "עולים על קו 5" · primary "עליתי לאוטובוס" (14 chars) · secondary "האוטובוס מאחר?" (14 chars).

### 3.7 ride
- **Hero:** the count, "עוד 3 תחנות", as a figure. **No plate, no band.**
- **412:** strip · eyebrow 88–123 "קו 5 לכיוון רידינג" · sentence 131–183 "אפשר לשבת בנחת." · sub 191–233 "אני אגיד מתי לרדת." · figure (hero, 96) centered ≈ 330–426 "עוד 3 תחנות" · card 450–571 (pin icon, name "דיזנגוף / ז'בוטינסקי", desc "כאן יורדים") · secondary 703–779 "ירדתי מהאוטובוס" · footer.
- **360:** figure 80; card name 2 lines max, nowrap parts.
- **Fixes:** (1) The plate+band holding "3" reads as "line 3", and it is the third bus-sign on the trip with a different meaning. (2) The band text "תחנות עד הירידה" wraps to 3 lines at 360. (3) The sentence "נשארו 3 תחנות" duplicates the hero. The sentence now gives comfort and the figure gives the number.
- **Copy:** "אפשר לשבת בנחת." · "אני אגיד מתי לרדת." (neutral) · figure prefix "עוד", unit "תחנות" (1 → "עוד תחנה אחת", see alert) · card desc "כאן יורדים".

### 3.8 alert
- **Hero:** "יורדים בתחנה הבאה!"
- **412:** column centered: icon 120 (≈ 210–330) · title 2 lines 362–496 · stop name 528–578 · button 610–730.
- **360:** title 56 still fits 2 lines ("בתחנה הבאה!" ≈ 300px). Button 120.
- **Fixes:** (1) Blue focus ring around "הבנתי" on yellow. Remove it (2.11). (2) Title breaks "בתחנה / הבאה יורדים!" with an orphan first word. Reorder and force the break as "יורדים / בתחנה הבאה!". (3) Remove the quotes around the stop name.
- **Copy:** "יורדים בתחנה הבאה!" · after tap: m "לחץ על כפתור העצירה." f "לחצי על כפתור העצירה."

### 3.9 off (got off?)
- **Hero:** the question.
- **412:** strip · eyebrow "קו 5 לכיוון רידינג" · sentence 131–183 "ירדת מהאוטובוס?" · sub 191–233 "אם כן, נמשיך ברגל." · card centered (stop name + "התחנה שלך") · primary 595–687 "כן, ירדתי" ✓ · secondary 703–779 "עוד לא" · footer.
- **Fixes:** (1) A single green button with no alternative looks like half of a broken pair. Make it primary blue, and add "עוד לא" (back to ride), which catches a mistaken tap. (2) At 360 the card name breaks "ז'בוטינ / סקי". Apply `overflow-wrap:normal` + nowrap parts. (3) "ירדת?" alone is too terse when read cold. Say "ירדת מהאוטובוס?".
- **Copy:** "ירדת מהאוטובוס?" (same spelling m/f) · "אם כן, נמשיך ברגל." · "כן, ירדתי" · "עוד לא".

### 3.10 finalwalk
- **Hero:** distance "150 מטר" + map. Mirror the walk screen exactly.
- **412:** strip · eyebrow "בדרך למרפאה" · sentence m "לך למרפאת כללית." / f "לכי למרפאת כללית." · figure row "150 מטר  כ־2 דקות" · map to 663 · primary 687–779 "הגעתי" (flag icon) · footer.
- **Fixes:** (1) The eyebrow "בדרך אל מרפאת כללית, דיזנגוף" wraps 2 lines at 360. Use the short kind. (2) There is no figure and the distance is buried in the sentence ("עוד 150 מטר ברגל, ואתה שם."), so it is inconsistent with walk. (3) The map label "מרפאת כללית, דיזנגוף" clips at the right edge. Use "המרפאה".
- **Copy:** as above.

### 3.11 arrived
- **Hero:** the destination name.
- **412:** strip (all done, muted) · title 88–148 "הגעת!" (48) · sub 156–198 "שמחתי לעזור." · card hero centered (flag icon, name 40 2 lines, desc "הדרך לקחה 18 דקות") · primary 595–687 "קח אותי הביתה" · secondary 703–779 "סיימתי" · footer.
- **Fixes:** (1) "18 / דקות" orphan. Nowrap the number+unit. (2) Four black done-discs dominate the top. Use the muted done style (2.1). (3) The card has a 60px dead zone under it. Center it in the hero band instead of top-aligning it.
- **Copy:** unchanged.

### 3.12 resume
- **Hero:** the trip card.
- **412:** "תכנון הדרך" · sentence 88–140 "להמשיך בדרך?" · card (flag, name, desc "באמצע הנסיעה בקו 5") · yes 579–671 "כן, ממשיכים" ✓ · no 687–779 "לא" ✗ · footer.
- **Fixes:** (1) "להמשיך את הדרך ל־מרפאת…" is wrong Hebrew: the maqaf+ל before a noun should be "למרפאת". It also runs 3 lines and repeats the card. (2) Desc "קו 5 · באוטובוס" is telegraphic. Write a sentence fragment. (3) No layout change.
- **Copy:** "להמשיך בדרך?" · "באמצע הנסיעה בקו 5" · "כן, ממשיכים" / "לא".

### 3.13 nodirect
- **Hero:** the person who can help (contact card), not the destination again.
- **412:** "תכנון הדרך" · sentence 88–192 "אין אוטובוס ישיר לשם." · sub "רותי יכולה לעזור." · contact card (initial disc "ר", "רותי", "050‑1234567" with U+2011 so it never splits) · primary 595–687 "להתקשר לרותי" · secondary 703–779 "לחזור להתחלה" · footer.
- **Fixes:** (1) The card repeats the destination with a vague "אין קו אחד שמגיע לשם". (2) "כדאי לבקש עזרה" is abstract. Name the person.
- **Copy:** as above. No contact saved: sub "אפשר להתקשר למוקד התחבורה הציבורית." with primary "להתקשר למוקד".

### 3.14 lost-landmark
- **Hero:** the landmark card.
- **412:** "איפה אני?" · sentence 88–140 m "אתה רואה את סופר־פארם?" / f "את רואה את סופר־פארם?" · landmark card centered (2.6) · yes 579–671 "כן, רואה" ✓ · no 687–779 "לא" ✗ · footer (one half tile).
- **360:** sentence 2 lines (was 4).
- **Fixes:** (1) The 3-line (4 at 360) question breaks "סופר־ / פארם" at the maqaf. Shorten it and use U+2011. (2) The card name repeats the question at the same weight. Fine to keep, since the card is the picture, but drop "בית המרקחת" from the question; the card says the kind. (3) The middot wraps to a line start. Use a comma.
- **Copy:** m/f above · desc "בית מרקחת, כ־25 מטר ממך" · "כן, רואה" (neutral).

### 3.15 lost-ask
- **Hero:** the mic.
- **412:** "איפה אני?" · sentence 88–140 m "מה אתה רואה לידך?" / f "מה את רואה לידך?" · sub 148–232 (2 lines) m "תגיד שם של חנות, רחוב או שלט." / f "תגידי …" · mic 160 centered ≈ 300–460 · field 484–560 · secondary 703–779 · footer.
- **Fixes:** (1) The secondary "צריך עזרה" is masculine-only. Use the infinitive "לבקש עזרה". (2) The field sits only 20px under the mic. Set a 24px gap (token). (3) The footer tile spans full width. Use half width at inline-start (2.9).
- **Copy:** secondary "לבקש עזרה".

### 3.16 help
- **Hero:** the contact card.
- **412:** "עזרה" · sentence 88–140 "רותי יכולה לעזור." · sub 148–190 m "שום דבר לא נשלח בלי שתלחץ." / f "…שתלחצי." · contact card centered · primary 595–687 "לשלוח איפה אני" (send icon) · secondary 703–779 "להתקשר לרותי" (phone icon) · footer (half tile).
- **Fixes:** (1) The primary "לשלוח לרותי איפה אני" wraps to 2 lines. The contact is already named in the sentence, so shorten it. (2) "בוא נקרא לרותי" is gendered and ambiguous ("נקרא" reads as *read*). (3) The phone icon on a non-tappable card. Use the initial disc.
- **Copy:** as above.

### 3.17 sent
- **Hero:** what was sent.
- **412:** "עזרה" · row: okdisc 72 + sentence m "שלחתי לרותי איפה אתה." / f "…איפה את." (2 lines, 88–192) · list 216–… 3 one-line rows · primary 595–687 "להתקשר לרותי" · secondary 703–779 "לחזור לדרך" · footer (half tile).
- **360:** okdisc 60. Rows stay 1 line with the shortened copy.
- **Fixes:** (1) Every list row wraps to 2 lines, giving a 296px list with uneven rhythm. Shorten the rows. (2) The divider runs under the icon. Inset it (2.7). (3) "כדאי לקחת קו 5" lacks the when. Add the minutes.
- **Copy:** rows "ליד סופר־פארם" · "בדרך למרפאת כללית" · "קו 5, בעוד 4 דקות".

### 3.18 offroute
- **Hero:** the map (you vs route).
- **412:** strip · eyebrow "בדרך לתחנה" · sentence 131–235 "נראה שהתרחקת מהדרך. לעזור לך?" · map 259–571 · primary 595–687 m "כן, תעזור לי" · secondary 703–779 "לא, אני בסדר" · footer (half tile).
- **Fixes:** (1) "לא, אני בסדר" in alarm red tells a calm person something is wrong. Use primary/secondary (2.8). (2) "כן, אני צריך עזרה" is masculine-only and 16 chars. (3) Map label "דיזנגוף / קינג ג'ורג'" clips. Use "התחנה".
- **Copy:** "נראה שהתרחקת מהדרך. לעזור לך?" (neutral) · "כן, תעזור לי" (addressed to the app, masculine app voice as elsewhere) · "לא, אני בסדר".

### 3.19 settings (one row per screen, 7 screens)
- **Hero:** the two options + a live preview.
- **412:** "הגדרות · 1 מתוך 7" · sentence 88–140 "גודל הכתב" · options row 164–256 (two `.opt`, gap 16, "גדול" ✓ / "ענק") · preview card 280–… showing a real sample ("עולים על קו 5" at the chosen size) · primary 595–687 "הבא" · secondary 703–779 "סיימתי" · footer.
- **Fixes:** (1) The preview is a 32px gray sub "כך נראה כתב גדול." that does not show the change. Replace it with a sample card. (2) "יציאה מההגדרות" is long and bureaucratic. (3) The selected option has a check but the unselected one has no affordance. Give both the 36px slot (empty for unselected) so the labels do not jump.
- **Copy:** secondary "סיימתי".

---

## 4. Do not (the 10 amateur tells, and the replacement)

1. **Two giant identical numbers on one screen** (stop: plate 5 at 120, countdown 5 at 96). → One hero per screen. A secondary figure is 72.
2. **The bus-sign plate used for a count** (ride "3"). → The plate is for line numbers only. Counts use the figure, without the band.
3. **The sentence repeating the card** (confirm, resume, nodirect, lost-landmark). → The sentence asks or instructs, and the card shows the thing. Never print the same name twice at 32+.
4. **Names broken mid-word** ("ז'בוטינ|סקי", "סופר־|פארם", "קינג|ג'ורג'"). → `overflow-wrap:normal` on names, nowrap spans per part, U+2011 in compounds.
5. **Button labels on 2 lines** (stop and ride at 360, help at 412). → Copy ≤ 14 chars at 360 with an icon. Shorten the words, never the type.
6. **Orphans and widows** ("18 / דקות", "בכל / פעם", "בתחנה / הבאה יורדים!"). → Nowrap number+unit, `text-wrap:balance`, forced break in the alert.
7. **Typographic noise**: quotation marks around stop names, "ק״מ", "דק׳", "·" middots, "(parentheses)". → Plain words, commas, a thin-spaced " / " between street names.
8. **Wrong color semantics**: red for the reassuring answer, a lone green button, a blue focus ring on the yellow alert. → Green/red only for fact-checks; primary/secondary otherwise; alert focus in currentColor.
9. **Raw OSM tiles and long names on the map** (purple carts and synagogue stars louder than the route; labels clipped). → Desaturated tiles, 8px route on a white casing, generic 32px labels ("התחנה", "אתה").
10. **Off-system details**: supporting text at weight 400 (§3 says ≥ 500), map labels at 30px, the amber edge at 2.45:1, a radius of 18 next to 16/20, and a demo badge sharing the top row with the strip. → The weights, sizes, colors and radii from §1. The badge becomes a footer tab.

---

## 5. Acceptance (measure, do not eyeball)

- Audit script at 412×915 and 360×780 on all 19 `?screen=` ids:
  - every text node is ≥ 32px, or 28 / 30 / 24 only for the listed roles;
  - computed `font-weight` ≥ 500;
  - every `button` is ≥ 72 tall and none has `getClientRects().length > 1` lines (label height ≤ 1.2 × font-size);
  - no element's `scrollWidth > clientWidth`.
- No `.say` exceeds 2 lines at 412 or 3 at 360 (`height / lineHeight`).
- The same y for `.say` top across all journey screens (±0px) and for `.actions` bottom (779 / 658).
- Contrast pairs as in §1.1 / §1.2; re-run `cr.py` on any new pair.
- Map: no `.lbl` rect outside `.map` rect after `fitBounds`.
