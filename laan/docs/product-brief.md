# Build "לאן?" — a one-instruction-at-a-time bus guide for elderly Israelis (Android)

## 0. Who this is for — the design north star

Users are Israelis aged roughly 75+, Hebrew speakers, on Android phones (often mid-range, 5–6.5", Chrome). Assume most of them have some of: reduced vision (cataract, presbyopia), hearing loss, hand tremor, slower processing, low confidence with apps, real fear of "pressing the wrong thing", and anxiety when lost. They do not use Moovit because it shows everything at once.

The app should behave like a patient grandchild standing next to them: one calm sentence, one thing to do, never blames, never shows technical language, never leaves them stuck.

Apply these rules everywhere, without exception:

1. **One decision per screen.** One primary button. At most one secondary action (smaller, but still ≥ 64px tall).
2. **Every instruction is spoken AND shown.** Never rely on a single channel (voice, text, vibration are redundant, not alternatives).
3. **Nothing happens silently or unexpectedly.** No auto-dismissing messages, no toasts, no modals, no timers that move the user forward (the only exception is the "get off" alert). No gestures: no swipe, long-press, pinch, double-tap, drag.
4. **Never a dead end.** Every screen can be heard again and can reach help.
5. **Plain Hebrew.** Second person, short common words, present tense, ≤ 12 words per sentence, one verb per sentence. No jargon, no abbreviations, no English anywhere on screen (not "GPS", not "OK"). Numbers as digits. Distances rounded to 50 m, minutes rounded, approximations with "כ־".
6. **Failure is invisible.** Any failed API call falls back silently (see §6). The user never sees an error code, a spinner longer than 8 seconds, or the word "שגיאה".
7. **Gendered Hebrew is handled**, not ignored: all strings live in one `STRINGS` object with masculine/feminine variants and a `t(key)` helper; the user picks once on first run.

## 1. Stack and constraints

- `index.html` — a single file, inline CSS and JS, no framework, no build step. Leaflet 1.9 from a CDN with OpenStreetMap tiles.
- `server.py` — Python 3 standard library only (`http.server`, `urllib.request`, `json`, `os`). Serves `index.html` and static files, binds `0.0.0.0:8000`, and proxies **every** external call so the browser only ever talks to the same origin (avoids CORS, keeps the API key on the server, gives one place to apply timeouts and fallbacks):
  - `POST /api/destination` → Claude: free speech → clean place query
  - `POST /api/where-am-i` → Claude: calm one-sentence orientation
  - `GET /api/geocode?q=` → Nominatim (`countrycodes=il`, `accept-language=he`, `limit=3`, bias to the user's viewbox). Send a descriptive `User-Agent` header — Nominatim rejects requests without one.
  - `GET /api/stops`, `GET /api/lines` → `open-bus-stride-api.hasadna.org.il` (GTFS stops and routes near a point)
  - `GET /api/walk?from=&to=` → `routing.openstreetmap.de/routed-foot` (walking geometry)
  - Every proxy: 6-second timeout, returns `{ "ok": false }` on any exception or non-200. Never passes raw upstream errors to the client.
- **Claude API** (raw HTTP from `server.py`): `POST https://api.anthropic.com/v1/messages` with headers `x-api-key: $ANTHROPIC_API_KEY`, `anthropic-version: 2023-06-01`, `content-type: application/json`. Model **`claude-fable-5-2`**. Do not send `thinking`, `temperature`, `top_p` or `top_k` (rejected on this model); send `output_config: {"effort": "low"}` and `max_tokens: 400` — these are tiny tasks. Check `stop_reason`: anything other than `end_turn` (including `refusal`) is treated as a failure → fallback. Ask for JSON in the system prompt and parse with `json.loads`; on parse failure → fallback. If `ANTHROPIC_API_KEY` is missing, the server starts anyway and every Claude route returns `{ok:false}` — the app must still work end to end.
- `manifest.json` + `sw.js` — installable PWA (name "לאן?", `display: standalone`, `orientation: portrait`, large icons). The service worker caches the shell so the app opens even offline; data calls go to the network.

## 2. Android-specific requirements

- Target Chrome for Android, test at 360×780 and 412×915 dp, portrait only. `<meta name="viewport" content="width=device-width, initial-scale=1">` — do **not** set `user-scalable=no`; sizes are large enough that zoom is unnecessary, but never block it. Use `100dvh`, respect safe areas, no horizontal scroll ever.
- **Secure context:** microphone and geolocation work only on `https` or `http://localhost`. On a phone over Wi-Fi they will not. The README must document the recommended test path: `adb reverse tcp:8000 tcp:8000`, then open `http://localhost:8000` in Chrome on the phone; alternatives: `chrome://flags/#unsafely-treat-insecure-origin-as-secure`, or an HTTPS tunnel. Demo mode must work on plain `http` (it needs neither mic nor GPS).
- **Speech recognition:** `window.SpeechRecognition || window.webkitSpeechRecognition`, `lang = "he-IL"`, `interimResults = false`, `continuous = false`. Show "אני מקשיב..." with a slowly pulsing ring while listening. Handle `no-speech`, `not-allowed`, `network` with plain Hebrew and offer the text field. If unsupported, hide the microphone and show only the keyboard field.
- **Text-to-speech:** `speechSynthesis` with a `he-IL` voice (voices load asynchronously — listen to `voiceschanged`), `rate 0.85`, `pitch 1`, always `cancel()` before speaking. Android Chrome blocks audio before a user gesture, so the first screen's button ("בוא נתחיל") also unlocks audio. If no Hebrew voice exists, show once: "הטלפון לא יודע לדבר עברית, אז ההוראות יופיעו בכתב." and continue text-only.
- **Vibration:** `navigator.vibrate([500,200,500,200,500])`, repeated every 5 s during the alert; a short `vibrate(30)` on every button tap as confirmation that the tap landed.
- **Wake lock:** `navigator.wakeLock.request("screen")` during the walk and the ride; re-acquire on `visibilitychange`.
- **State survives interruptions:** keep the whole journey in `localStorage`. A phone call, screen lock, accidental home or back, or a reload must never lose the trip. On reopen: "להמשיך את הדרך ל־<destination>?" with כן / לא.
- **Android back button:** intercept with `history.pushState` + `popstate`. Never exit silently — show "לעצור את הדרך?" with big לא (default, top) / כן.
- **Geolocation:** `watchPosition({enableHighAccuracy: true, maximumAge: 5000})`. Ignore fixes with accuracy > 60 m for stop counting. A stop counts as passed when within 40 m of it. Keep a manual fallback button on every tracking screen ("הגעתי לתחנה", "עליתי על האוטובוס") because indoor/urban GPS is unreliable.
- Performance: no frameworks, minimal JS, lazy-create the map only when needed. Must feel instant on a mid-range phone.

## 3. Visual and interaction spec

**Typography** — system stack with Hebrew support (`"Noto Sans Hebrew", Roboto, Arial, sans-serif`). Body ≥ 32px; the instruction sentence 40px/700; headings 44px; the bus line number and "stops left" number 96px/800 in a white box with a black border, like a real bus sign. Line height 1.35. Font weight never below 500. No thin, light or condensed styles, no gray text lighter than `#444`.

**Sizing** — buttons full-width, `min-height: 88px`, 24px vertical gap, 20px radius, anchored to the bottom of the screen (thumb zone), 20px side margins. Every touch target ≥ 72×72 px. Text fields 72px tall with 36px text. Debounce taps 600 ms so a tremor does not register as a double tap.

**Color** — WCAG AAA (≥ 7:1) everywhere. Light theme: background `#FFFFFF`, text `#111111`, primary action deep blue `#0B3D91` with white text. "כן"/go = green `#1B7F3B`; "לא"/stop = red `#B00020` — always color + word + symbol (✓ ✗), never color alone. Alert screen alternates `#FFD600` and `#000000` at 1 Hz with 56px text. A "שחור־צהוב" high-contrast theme (black background, yellow text) is available in settings. No gradients, no decorative shadows, no disabled-looking buttons.

**Screen layout** (identical on every screen, so the user always knows where to look): small step label at top (28px, e.g. "שלב 2 מתוך 4") → one instruction sentence → map or the big number, when relevant → primary button → secondary button if any → a persistent footer row with two buttons, each ≥ 72px tall: "🔊 תקרא שוב" and "😕 אני לא בטוח איפה אני".

**Icons** only with a text label. Emoji are fine as supplementary cues (🎤 🔊 🏠 📞), never as the only meaning.

**Motion** — none, except the mic pulse and the alert flash. Respect `prefers-reduced-motion` (the alert then flashes at 0.5 Hz instead of stopping — it is a safety signal).

**Hebrew RTL** — `<html lang="he" dir="rtl">`, logical CSS properties only (`margin-inline-start`, `padding-inline-end`, `text-align: start`), numbers and line numbers wrapped in `<bdi>`. The text field uses `dir="auto"`.

**Map** — secondary, never the hero. Big blue "אתה" dot with a label, the stop as a large pin with its name, the walking route as an 8px line. Panning only; no zoom buttons, no layer controls, no attribution overlay covering content (keep attribution small at the bottom edge).

**Never use:** hamburger menus, tabs, dropdowns, carousels, toasts, modals, bottom sheets, infinite scroll, skeleton loaders, small "×" close buttons, text links, cookie banners, login, onboarding carousels, icons without labels.

## 4. The flow — screens, exact copy, voice

Every screen speaks its sentence automatically 300 ms after it appears; "תקרא שוב" repeats it. Strings below are the masculine form; provide feminine variants.

**Screen 0 — first run only (never again):**
1. "שלום! אני אעזור לך להגיע בקלות." → button "בוא נתחיל" (also unlocks audio).
2. "איך לפנות אליך?" → two big buttons "אתה" / "את". Stored.
3. "איפה הבית שלך?" → mic + text field, geocode, confirm. Needed for "קח אותי הביתה". "לא עכשיו" is allowed — then ask when the home button is first pressed.
4. "למי להתקשר אם צריך עזרה?" → phone field (36px digits, numeric keyboard), "לא עכשיו" allowed. Used by the help screen as a `tel:` button.
5. Permission explanation **before** the browser asks: "כדי להדריך אותך אני צריך לדעת איפה אתה ולשמוע אותך. עכשיו הטלפון ישאל — לחץ 'אפשר'." → button "בסדר", then request location and microphone.

**Screen 1 — destination:** "לאן אתה צריך להגיע?" A round microphone button, 160px, centered; under it a text field with placeholder "או כתוב כאן" (keyboard-safe: the field scrolls into view when focused). States: "אני מקשיב..." → "רגע, אני בודק...". Send the transcript to Claude with a system prompt: *user is in Israel, speaking Hebrew; strip filler ("אני צריך להגיע ל", "בבקשה", "תביא אותי"); resolve common phrasings (e.g. "קופת חולים בדיזנגוף" → a clinic on Dizengoff St, Tel Aviv; add the user's city, passed from reverse geocoding, when no city is said); return JSON only: `{"query": "<Nominatim query>", "display_name": "<short Hebrew name to read aloud>"}`.* Then geocode. If nothing is found: "לא מצאתי את המקום. אפשר לומר שוב, או להגיד את שם הרחוב והעיר." — never an error code.

**Screen 2 — confirm:** "הבנתי: <display_name>. נכון?" plus "זה כ־3 ק״מ מכאן." Buttons: "כן ✓" (green, on top) / "לא ✗" (red). "לא" returns to Screen 1 with the field prefilled.

**Screen 3 — find a direct bus and walk to the stop:** "רגע, אני מחפש לך אוטובוס..." with a slow calm progress bar, at most 8 s before falling back. Logic: stops within 500 m of the user and within 500 m of the destination (Stride); routes that serve one stop from each set in the right direction (same trip, origin `stop_sequence` < destination `stop_sequence`); choose the route with the shortest total walking. **Direct lines only — never show or suggest a transfer.** If none exists: "אין אוטובוס ישיר מכאן. כדאי לבקש עזרה." with "📞 התקשר ל־<contact>" and "חזור". Then show the map with the walking line and one sentence: "לך 250 מטר לתחנה 'דיזנגוף/ארלוזורוב'. זה כ־4 דקות." Primary: "יצאתי לדרך". Tracking advances automatically within 30 m of the stop; manual fallback "הגעתי לתחנה".

**Screen 4 — at the stop:** "עלה על קו <N>" with N at 96px in the bus-sign box, "לכיוון <headsign>", and "מגיע בעוד M דקות (לפי לוח הזמנים)" counting down every 30 s. Primary: "עליתי על האוטובוס". Secondary: "האוטובוס לא מגיע?" → "לפעמים האוטובוס מתאחר. אפשר לחכות עוד כמה דקות או לבקש עזרה." with the call button.

**Screen 5 — riding:** "נשארו <K> תחנות" with K at 96px, below it "אפשר לשבת בנחת. אני אגיד לך מתי לרדת." K updates as GPS passes stops (40 m radius). When K = 1: full-screen flashing alert "בתחנה הבאה יורדים!" — spoken every 5 s, vibration pattern every 5 s, until "הבנתי" (88px) is pressed; then "לחץ על כפתור העצירה באוטובוס." At the destination stop: "ירדת?" → "כן, ירדתי". If GPS shows the stop was passed: "נראה שעברת את התחנה. אל דאגה — רד בתחנה הבאה, ואני אדריך אותך בחזרה." and re-plan the final walk from there.

**Screen 6 — final walk:** "עוד 120 מטר ברגל, ואתה שם." with the map; auto-advance within 30 m, manual "הגעתי".

**Screen 7 — arrival:** "הגעת! 🎉" Primary: "🏠 קח אותי הביתה" (runs the same flow with home as destination, skipping Screens 1–2). Secondary: "סיימתי".

**Persistent "😕 אני לא בטוח איפה אני":** pauses tracking, shows "רגע, אני בודק איפה אתה..." and sends to Claude: lat/lon, nearest street (Nominatim reverse), current step, route summary. System prompt: *answer in ONE sentence of at most 14 simple Hebrew words, calm, concrete, say where the user is and what to do next; no questions, no apologies, no technical words.* Shown at 40px and spoken. Buttons: "הבנתי, ממשיכים" and "📞 התקשר ל־<contact>" (`tel:`). If Claude fails, build the sentence locally from the data: "אתה ברחוב <street>, ליד <stop>. המשך <next step>."

**Settings** (reachable from a "הגדרות" button on Screen 1 only, as two-button toggles, each row one choice): text size (גדול / ענק — the latter scales everything ×1.25), contrast (רגיל / שחור־צהוב), voice (כן / לא), speech speed (רגיל / איטי), home address, help contact, אתה/את.

## 5. Demo mode — `?demo=1`

- Skips mic and geolocation entirely (no permission prompts), uses the fallback route from §6, and after 2 s fills "קופת חולים בדיזנגוף" as if spoken. The confirm screen waits for a tap (with `&auto=1` it taps "כן" after 3 s so the demo runs hands-free).
- A simulated position moves along the walking path (~15 s), waits at the stop while the countdown runs fast (~10 s), rides through the stops (~40 s, triggering the real alert with voice and vibration), final walk (~10 s), arrival. Whole journey ≤ 90 s; `&speed=2` halves it.
- Small "דמו" badge (24px) in a corner. Everything else — voice, vibration, screens, copy — is identical to real mode.
- Must work fully offline (if map tiles fail, show a plain light background; the rest continues).

## 6. Hardcoded fallback route (Tel Aviv)

Define a `FALLBACK_ROUTE` constant with approximate real coordinates along Dizengoff St (mark them approximate in a comment): user start near Dizengoff Center; origin stop "דיזנגוף/קינג ג'ורג'"; line **5** (Dan) toward "רידינג"; intermediate stops with real names (דיזנגוף/בוגרשוב, דיזנגוף/פרישמן, דיזנגוף/גורדון, דיזנגוף/ארלוזורוב, דיזנגוף/ז'בוטינסקי); destination stop near a clinic on Dizengoff; a ~250 m walking polyline to the origin stop and ~120 m from the destination stop; scheduled departure "in 6 minutes".

Fallback is **per step**: if Claude fails, use the raw transcript as the query; if Nominatim fails, use the fallback destination; if Stride fails, use the fallback line and stops; if OSRM fails, draw a straight line and estimate meters by haversine. The user sees nothing technical — the wording "לפי לוח הזמנים" already covers the scheduled-time case.

## 7. Verification before you finish

Run `server.py`, open `http://localhost:8000/?demo=1&auto=1` in Chrome device emulation (Pixel 7, 412×915, and a small 360×780) and complete the whole journey. Confirm with evidence (console logs / a small audit script run in the page), not by eye:

- No horizontal scroll on any screen; every rendered text ≥ 32px (audit `getComputedStyle` of all visible text nodes); every button ≥ 72px tall; all text/background pairs ≥ 7:1.
- `speechSynthesis.speak` is called on every screen entry (log it); `navigator.vibrate` is called at the alert; the alert persists until "הבנתי" is tapped.
- Android back is intercepted; a reload mid-ride resumes the journey; both themes and both text sizes render without overflow.
- Kill the network (block the upstream hosts in the proxy) → the full journey still completes via fallback with no visible error. Unset `ANTHROPIC_API_KEY` → same.
- Lighthouse accessibility ≥ 95.

Deliver `index.html`, `server.py`, `manifest.json`, `sw.js`, an icon, and a short `README.md` with run instructions (including `adb reverse`), and a one-paragraph list of what was verified. Do not add analytics, accounts, frameworks, or a build step.
