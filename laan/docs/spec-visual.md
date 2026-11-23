# לאן? — visual refinement + full phone mockup (round 2, read with spec-ui.md and spec-round2.md)

Yosi's ask: "clear, big and simple — but professional, not something that looks generated". The first build
works but reads as a wireframe: big empty middle, every button the same outlined box, emoji as icons, a hard
black rule above the footer, no sense of where you are in the journey. Fix the visual system, keep every size
minimum (text ≥ 32px except the micro-labels listed below, buttons ≥ 72px, AAA contrast).

## 1. Visual system

- **Reference stays the Israeli bus-stop sign / road signage** — make it visible: the line number lives in a
  sign plate (white plate, 4px ink border, radius 10px, Secular One 96px) set on a yellow #FFD400 band like the
  real stop poles; the stop name sits under it like the sign's caption.
- **Real icons, no emoji.** Inline SVG icon set (one `<symbol>` sprite in the page): mic, speaker, compass,
  phone, map-pin, home, bus, walk, flag, check, x, gear, send, clock. 24×24 viewBox, stroke 2.5, round caps and
  joins, `currentColor`, rendered at 36–44px. Direction icons (arrow, chevron) mirror in RTL; objects don't.
- **Journey strip** at the top of every journey screen (walk → stop → bus → arrive): four 44px icons joined by
  a line; done = ink filled, current = blue filled with a 4px ring, next = outlined muted. Gives the person a
  constant "where am I in the trip". Under it the step label ("שלב 2 מתוך 4 · בתחנה") at 28px, color #5A5246.
  Onboarding screens use a simple 5-dot progress instead.
- **Instruction block**: sentence 44px Secular One, line-height 1.3, ink; supporting line 32px Miriam Libre 500,
  #3A342C. Vertically place the block in the upper-middle third — not glued to the top with a void below.
  Fill the middle with meaningful content only: the sign plate, the map, the big number, or a calm
  illustration-like icon in a 160px soft circle (#EFE6D3) — never empty space.
- **Buttons — three tiers, visually distinct:**
  - Primary: solid #0B3D91, white Secular One 36px, min-height 92px, radius 18px, a 6px darker bottom edge
    (#072A66) that collapses to 2px on press (tactile, like a physical button). Icon at the inline-start.
  - Yes/No pairs: green #1B7F3B / red #B00020 solid, same shape, with check / x icons; yes always on top.
  - Secondary: #FFFFFF fill, 3px ink border, ink text 32px, min-height 76px.
  - Quiet (settings, "לא עכשיו"): no border, underlined ink text 30px, min-height 60px, at the very bottom.
- **Footer** is a tinted bar (#EFE6D3, no black rule), safe-area padded, two side-by-side tiles each ≥ 88px:
  "לשמוע שוב" (speaker icon, white tile) and "איפה אני?" (compass icon, amber tile #FFE7A3 with ink border —
  help is visually distinct and always findable). Icon on top, label below at 30px (micro-label exception), one
  line each at 360px width — measure it.
- **Settings**: only as a Quiet button at the bottom of the destination screen ("הגדרות" with gear icon).
- **Alert**: keep the 1 Hz #FFD400/#111 flash, add the bus icon at 120px and "בתחנה הבאה יורדים!" at 56px.
- **Elevation & separation**: whitespace first, then #F3ECDF panels with radius 20px; no 1px grey borders, no
  drop-shadow soup. Map in a panel with radius 20px, max 38vh.
- **Ground** #FBF7EF, ink #1B1B1B. High-contrast theme unchanged (black/yellow) but icons and plates follow it.
- Fonts: Secular One (display, buttons, numbers) + Miriam Libre 400/500/700 (text). Keep the fallback stack.

## 2. Deep links for the mockup — `?screen=<id>`

Add a `?screen=` parameter (implies demo data, no permissions, no auto-advance, voice off unless `&voice=1`) that
renders any single screen directly with realistic demo content. Required ids:

`welcome, gender, home, contact, perms, dest-first, dest-return, listening, confirm, planning, walk, stop, ride,
alert, off, finalwalk, arrived, resume, nodirect, notfound, lost-calm, lost-landmark, lost-ask, lost-orient,
help, sent, offroute, settings, exit`

`dest-return` shows "שלום שוב! לאן היום?" with the home + 2 recent shortcuts. `sent` shows the ✓ + the
three-line summary. `offroute` shows "נראה שהתרחקת מהדרך. צריך עזרה?".

## 3. Mockup page — `/Users/26yos/at/laan/mockup.html`

A presentation page (not part of the app flow) showing every screen above inside realistic Android phone frames:
each frame is an `<iframe src="index.html?screen=<id>" width=412 height=915>` scaled to ~0.5 with CSS transform,
inside a device bezel (dark rounded body, punch-hole camera, 28px radius), with a Hebrew caption under each phone
(screen name + one line on why it is designed that way, 20px — this page is for Yosi, not for elderly users).
Group into sections with headings: "כניסה ראשונה", "כניסה חוזרת", "הדרך", "אני לא בטוח איפה אני", "עזרה מאדם",
"מצבי קצה". RTL, same fonts and ground as the app, responsive grid (1 column on phones, 3–4 on desktop). Add a
"▶ דמו חי" link to `index.html?demo=1&auto=1` at the top.
