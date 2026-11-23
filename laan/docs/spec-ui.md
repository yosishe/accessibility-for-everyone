# לאן? — UI implementation spec (read with /Users/26yos/at/laan-prompt.md)

The product brief is `/Users/26yos/at/laan-prompt.md`. This file adds the decisions already
made by the orchestrator so that `index.html` matches `server.py` and the design lock.

## Design lock (binding)

```
Reference : Israeli bus-stop sign + road signage — one giant number in a box, warm ground, one word.
Color     : ground #FBF7EF (warm cream, never pure white) · ink #1B1B1B · action blue #0B3D91 (white text)
            · signage yellow #FFD400 for the alert only · yes-green #1B7F3B · no-red #B00020.
            High-contrast theme: ground #000000, ink/buttons #FFE14D with #000 text.
Type      : "Secular One" (Google Fonts) for the big numbers, screen sentences and button labels;
            "Miriam Libre" 400/700 for body/secondary text. Fallback stack: Arial, sans-serif.
            Load via <link> with display=swap; the app must look right if fonts never load.
Layout    : every screen = [step label 32px] [one sentence 40px bold] [optional map / big number]
            [primary button 88px] [optional secondary 72px] [fixed footer: "🔊 תקרא שוב" | "😕 אני לא בטוח איפה אני"].
            Bottom-anchored actions (thumb zone). 100dvh, no page scroll, no horizontal scroll.
Risk      : no navigation at all — no menu, no on-screen back. The only way forward is the primary button.
```

Sizes: body ≥ 32px everywhere (the only exception is Leaflet's attribution control), sentence 40px/700,
numbers 96px, buttons `min-height: 88px` full width, footer buttons `min-height: 72px`, inputs 72px tall
with 36px text, 20px side margins, 24px gaps, radius 20px (buttons) / 12px (sign box). Tap feedback:
button darkens + `navigator.vibrate(30)`. Debounce clicks 600 ms (tremor). `prefers-reduced-motion`
respected except the alert, which then flashes at 0.5 Hz.

RTL: `<html lang="he" dir="rtl">`, logical CSS properties only, `<bdi>` around numbers, `dir="auto"` on inputs.
Never end a Hebrew line with a Latin token. No English visible anywhere in the UI.

## server.py API contract (already implemented, do not change the server)

All same-origin. Every response has `ok`. `ok:false` → use the fallback for that step, silently.

- `POST /api/destination` body `{text, city}` → `{ok, query, display_name}`
- `POST /api/where-am-i` body `{lat, lon, street, step, route, gender}` → `{ok, text}`
- `GET /api/geocode?q=&lat=&lon=` → `{ok, found, lat, lon, name}` (`found:false` = place not found → ask again; `ok:false` = service down → fallback destination)
- `GET /api/reverse?lat=&lon=` → `{ok, street, city}`
- `GET /api/walk?from=lat,lon&to=lat,lon` → `{ok, meters, path:[[lat,lon],...]}`
- `GET /api/plan?olat=&olon=&dlat=&dlon=` → `{ok, line, headsign, origin_stop:{name,lat,lon}, dest_stop:{name,lat,lon}, stops:[{name,lat,lon}...], departs_in_min}` ; `{ok:false, reason:"no-direct"}` means the data worked but there is no direct line → show the "אין אוטובוס ישיר" screen (real mode only); any other `ok:false` → fallback route.
- `GET /api/health` → `{ok, claude}`

## State machine

`settings` (localStorage `laan.settings`): `{done, gender:'m'|'f', home:{name,lat,lon}|null, contact:string|null, size:'l'|'xl', contrast:'normal'|'hc', voice:true, rate:0.85|0.7}`.
`journey` (localStorage `laan.journey`): `{dest:{name,lat,lon}, plan, walkTo:{meters,path}, walkFrom:{meters,path}, step:'walk'|'stop'|'ride'|'off'|'finalwalk'|'arrived', passedIdx:-1, departsAt:ms}`.
Save after every change. On load: if `!settings.done` → welcome flow; else if `journey && journey.step !== 'arrived'` → resume screen "להמשיך את הדרך ל־<dest>?"; else → destination screen.

Screens (all copy and gender variants are in the brief §4; add a `g(m,f)` helper and keep every string in one `STRINGS`/`t()` place):
welcome → gender → home → contact → perms → dest → confirm → planning → walk → stop → ride → (alert overlay) → off → finalwalk → arrived. Plus: help (overlay), settings, exitConfirm (Android back), resume, nodirect, notfound (inline on dest).

Position handler (`onPos(lat, lon, accuracy)`, same function for GPS and the demo simulator):
- ignore fixes with accuracy > 60 m for stop counting; always move the map marker.
- `walk`: within 30 m of `origin_stop` → stop screen. Manual button "הגעתי לתחנה".
- `ride`: `stops` = plan.stops (after origin, destination last). For each index > passedIdx within 40 m → passedIdx = index. K = stops.length − passedIdx − 1. K === 1 → alert overlay (voice every 5 s, `vibrate([500,200,500,200,500])` every 5 s, flashing #FFD400/#000, until "הבנתי"). passedIdx === last → off screen "ירדת?". Manual secondary "ירדתי מהאוטובוס".
- `finalwalk`: within 30 m of dest → arrived. Manual "הגעתי".
Stop screen countdown: `departsAt = now + departs_in_min*60000`, shows `ceil((departsAt−now)/60000)` minutes, "מגיע עכשיו" at 0, refresh every 30 s (demo: 1 simulated minute = 2 s).

Voice: `speak(text)` → `speechSynthesis.cancel()` then speak with a he-IL voice (handle `voiceschanged`), rate from settings. Speak each screen's sentence 300 ms after it appears. "תקרא שוב" repeats the current sentence. If no he-IL voice: show once "הטלפון לא יודע לדבר עברית, אז ההוראות יופיעו בכתב." and continue.

Android: wake lock during walk/ride (re-acquire on visibilitychange); `history.pushState` + `popstate` → exitConfirm when a journey is active (default button is "לא"); register `sw.js`; `<link rel="manifest" href="manifest.json">`; theme-color #0B3D91.

Map (Leaflet 1.9.4 from unpkg or cdnjs, created lazily when first needed, reused): user = big blue dot (28px) with label "אתה/את", stop = large pin with name, walking path = 8px blue line, `zoomControl:false`, dragging on, fit bounds with padding. The map is max 40% of the screen height; the sentence and the button stay visible.

## Demo mode (`?demo=1`, `&auto=1`, `&speed=`)

No permission prompts. Position comes from a simulator that animates along a path and calls `onPos`.
Timeline (×1/speed): fill the text field with "קופת חולים בדיזנגוף" after 2 s as if spoken → confirm
(auto: tap "כן" after 3 s) → planning uses FALLBACK (skip network entirely in demo) → walk animation 15 s
to the origin stop → stop screen, countdown ticking fast (auto: tap "עליתי על האוטובוס" after 10 s) →
ride animation ~40 s through the stops; alert at K=1 (auto: "הבנתי" after 4 s) → off screen (auto: tap after 3 s)
→ final walk 10 s → arrived. Total ≤ 90 s. Without `auto`, the simulator pauses at each tap and waits for the user.
Show a 32px "דמו" badge in a corner. Voice and vibration behave exactly as in real mode.

## FALLBACK_ROUTE (approximate coordinates along Dizengoff St, Tel Aviv — mark as approximate in a comment)

```
start:        32.0753, 34.7752   (near Dizengoff Center)
origin_stop:  "דיזנגוף/קינג ג'ורג'"   32.0762, 34.7748
line: "5", headsign: "רידינג"
stops (after origin, destination last):
  "דיזנגוף/בוגרשוב"     32.0775, 34.7746
  "דיזנגוף/פרישמן"      32.0810, 34.7735
  "דיזנגוף/גורדון"       32.0830, 34.7730
  "דיזנגוף/ארלוזורוב"    32.0870, 34.7720
  "דיזנגוף/ז'בוטינסקי"   32.0890, 34.7715   ← dest_stop
dest: "מרפאת כללית, דיזנגוף"  32.0895, 34.7732
departs_in_min: 6
walkTo: straight path start→origin_stop with 2 intermediate points (~250 m); walkFrom: dest_stop→dest (~120 m).
```

Per-step fallback: Claude fails → use the raw transcript as the query; geocode `ok:false` → FALLBACK.dest;
plan `ok:false` (not "no-direct") → FALLBACK plan; walk fails → straight line + haversine meters.

## Deliverable

One file: `/Users/26yos/at/laan/index.html` (inline CSS + JS, no build step, no framework). It must load
and run the whole demo with `python3 /Users/26yos/at/laan/server.py` on http://localhost:8000/?demo=1&auto=1
and also when opened with no network (fonts/tiles missing is fine). Before reporting, run the server, open the
demo in a headless browser (the `playwright` MCP tools are available, or `python3 -m webbrowser` is not — use
playwright or curl + a JS audit if you can), and confirm: the demo reaches "הגעת!" in ≤ 90 s; no horizontal
scroll; min computed font size of visible text (excluding `.leaflet-control-attribution`) ≥ 32px; every
`button` height ≥ 72px; `speechSynthesis.speak` called on each screen (stub it and count); `navigator.vibrate`
called at the alert. Fix what fails. Report what you verified and what you could not.
