# לאן? — professional polish (Yosi #22: "not professional enough") — overrides spec-visual where they conflict

Diagnosis from the 412×915 screenshots (/Users/26yos/at/laan-shots/*.png):
1. **One single-weight display face everywhere (Secular One)** → no hierarchy by weight; every line shouts. This is the main reason it looks amateur.
2. **The key fact is not the biggest thing.** On the stop screen the minutes-until-arrival sit in small body text while the heading, the plate and the direction all compete.
3. **Crowded sign card**: direction + stop name wrap into 4 ragged lines beside the plate; "דיזנגוף/ קינג ג'ורג'" breaks at the slash.
4. **Heavy 3px black outlines** on secondary buttons and footer tiles read as a wireframe; the amber "איפה אני?" tile and the white tile look like two different systems.
5. **Decorative filler**: icon-in-a-beige-circle on arrived / lost / offroute screens.
6. Uneven vertical rhythm between screens; "דמו" badge collides with the journey strip; the map is too small to read.

Reference direction: **a calm transit app for grandparents** — the clarity of Citymapper / Apple Maps transit cards, with Israeli bus-stop signage as the one signature element. Quiet surfaces, one strong number per screen.

## Changes
- **Type:** switch the UI face to **Rubik** (Google Fonts, weights 400/500/700/800 — real Hebrew support, variable weight ⇒ hierarchy by weight). Keep **Secular One only for the line-number plate and the big countdown digits**. Body/supporting text Rubik 400–500, sentence Rubik 700, buttons Rubik 700. Scale: 32 / 40 / 48 / 120 (plate) / 96 (countdown). Line-height 1.3 for 32–48px Hebrew. `text-wrap: balance` on sentences; never break a stop name at "/": render "דיזנגוף / קינג ג'ורג'" with thin spaces and `white-space: nowrap` per part.
- **One hero fact per screen**, biggest on screen:
  - stop: the plate (line 5, 120px) as the hero, then on ONE line "לכיוון רידינג", then the countdown as a big figure "בעוד **5** דק׳" (digits 96px, label 32px) with "לפי לוח הזמנים" 28px muted under it. The stop name moves to the step label row ("בתחנה דיזנגוף / קינג ג'ורג'").
  - walk: distance "250 מ׳" big + "4 דק׳ הליכה", map below, larger (≥ 42% of height) with heavier labels.
  - ride: "3" big with "תחנות עד הירידה", the destination stop as one line.
  - arrived: replace the circle filler with the destination name as the hero ("מרפאת כללית, דיזנגוף") under "הגעת!" and the time it took ("הדרך לקחה 18 דקות").
  - lost/offroute: replace filler circles with content — the landmark card (photo-like icon + name + distance) or a small schematic showing "you" relative to the route.
- **Surfaces, not outlines:** secondary buttons = solid surface (#EFE7D8 light / #2A251E dark) with ink text, no border; focus ring 4px blue offset 2px. Primary keeps solid blue with the tactile 4px bottom edge (not 6px). Yes/no keep green/red solids. Remove all 3px black outlines except the sign plate.
- **Footer:** one calm bar, two equal tiles in the same style (surface #FFFFFF on bar #EFE7D8), "איפה אני?" distinguished by an amber icon disc and amber 4px top edge, not a different tile fill. 88px tall, icon 32 + label 30.
- **Top row:** journey strip right-aligned (RTL start) with 36px icons; "דמו" badge moved to the bottom-start corner above the footer, 24px, muted — it is not part of the product.
- **Rhythm:** fixed layout grid per screen: top row 56px · 24 · sentence block · 24 · hero block (flex 1, centered) · 24 · actions · footer. Same y for sentence and actions on every screen. Spacing tokens 8/16/24/32/48 only.
- **Color tuning:** ground #F7F3EC, surface #FFFFFF, surface-2 #EFE7D8, ink #1A1814, ink-2 #4A443B (≥ 7:1 on ground), blue #0B3D91, yellow #FFD400 only for the plate band and the alert. Shadows: one soft elevation for cards only (0 1px 2px rgba(26,24,20,.08), 0 8px 24px rgba(26,24,20,.06)).
- Re-measure after the change: min text 32 (28 allowed for step label, footer label, "לפי לוח הזמנים"), buttons ≥ 72, contrast ≥ 7:1, no horizontal scroll at 360.
