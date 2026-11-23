# לאן? — the Artifact build (Claude-hosted app, phone-first)

Deliverable: `/Users/26yos/at/laan/artifact/laan.html` — a published claude.ai Artifact that IS the app, derived
from the finished round-2 `/Users/26yos/at/laan/index.html` (same screens, copy, visual system, flow), adapted to
the Artifact frame. Yosi wants an Artifact (not a local HTML file), with a more precise UI, fitted to and shown
at phone size.

## Page contract (Artifact rules, binding)
- No `<!doctype>/<html>/<head>/<body>`; start with `<title>לאן?</title>`, `<meta name="claude:viewport-fit-sides" content="cover">`, then `<style>`.
- Wrapper element gets `lang="he" dir="rtl"` (no html tag to put it on).
- Scripts only from cdnjs/jsdelivr/unpkg pinned exact versions; fonts only Google Fonts (Secular One, Miriam Libre) with fallbacks. No other network: **no fetch to /api, Nominatim, Stride, OSRM, Overpass; no map tiles; no service worker; no manifest**.
- **No Leaflet.** Replace the map with an inline SVG schematic drawn from the route coordinates (project lat/lon to the box): streets as soft lines, walking path dashed blue 8px, bus path solid, stops as circles with names, "you" as a pulsing blue dot (reduced-motion: static). It looks like a clean transit diagram, not a broken map.
- Device APIs refused unless declared: geolocation, SpeechRecognition, Web Share, vibrate are unavailable → journey always runs on the demo simulator (FALLBACK route on Dizengoff) with manual buttons; vibration calls wrapped in try/catch (harmless no-op).
- `tel:`/`sms:` unreliable in the frame → help screen shows the contact's number as large selectable text with a "להעתיק את המספר" copy button, and the message to send (location + destination + which line) as a text panel with "להעתיק את ההודעה". Keep `tel:`/`sms:` links as a convenience but never claim "נשלח"/"מתקשר" because of a tap. The "sent" screen becomes "ההודעה מוכנה — להדביק בוואטסאפ לבן" after a successful copy.
- `alert/confirm/prompt` don't exist → all confirmations in-page (already so).
- localStorage wrapped in try/catch; app renders correctly without it.
- Theme: tokens on `:root` (light), dark via `@media (prefers-color-scheme: dark) :root:not([data-theme="light"])` and `:root[data-theme="dark"]`, with `color-scheme: dark`; body background from a token. Dark palette: ground #121212-ish warm (#16130F), ink #F4EFE6, action blue lightened (#6E9BFF on dark with #0B1430 text, or keep #0B3D91 buttons with white text — must stay ≥ 7:1), yellow alert unchanged. The in-app "שחור־צהוב" high-contrast setting still overrides.
- Size the app with `height: 100%` on the wrapper (not 100vh) inside the `:root` safe-area padding.

## Capabilities (declare at publish: `{sample:{}, dictation:{}, tts:{}}`)
Include `/Users/26yos/at/laan/claude-host.js` INLINE in the page (no separate file), so `window.LaanHost` exists:
- `understand` (Claude parses the spoken destination), `whereAmI` (calm sentence, landmark match), `dictation` (mic), `speak` (Claude voice, `language: "he"`; when it returns false fall back to speechSynthesis he-IL).
- `claude.use()` resolves late or null → the page must render and work fully before/without it (typing instead of mic; on-screen text if no voice).
- Mic button: call `LaanHost.dictation.start` synchronously inside the click handler.
- Demo nearby landmarks for the "איפה אני?" flow are canned (סופר־פארם, בנק לאומי, כיכר דיזנגוף).

## Phone presentation
- On a phone (≤ 600px wide): the app fills the screen edge to edge — this is the product.
- On desktop/tablet: center the app inside a realistic Android phone body (412×915 logical, dark bezel 12px, radius 44px, punch-hole camera, subtle shadow), scaled to fit the viewport height (`min(1, (100vh-48px)/939)`); beside it (≥ 1100px wide) a narrow side panel with: "▶ להתחיל דמו" (runs the hands-free 90-second journey), a "קפיצה למסך" list of the screen ids (first run, return visit, walk, stop, ride, alert, arrived, איפה אני, help, offroute) that jumps the phone to that screen, and a toggle אתה/את. On narrower desktops the panel moves under the phone. The panel uses the same tokens and fonts but small sizes (16–18px) — it is for the presenter, not the elderly user.
- First frame (thumbnail) shows the phone on the destination return-visit screen with real content, not an empty shell.
- Route the presenter's jumps on `location.hash` (`#walk`, `#ride`, `#lost-landmark`… ASCII ids only, none of the reserved words).

## UI precision pass (on top of spec-visual.md)
Measure and fix, don't eyeball: every text/background pair ≥ 7:1 in both themes and HC; all text ≥ 32px inside the phone except allowed micro-labels (≥ 28px); buttons ≥ 72px; consistent 8-pt spacing (8/16/24/32/48); the same vertical rhythm on every screen (journey strip → sentence → content panel → actions → footer at identical y positions across screens so the eye never hunts); one primary per screen; icon sizes 36/44 only; sign plate and stop captions aligned to the same inline-start edge; no orphan single words on the 44px sentence (use `text-wrap: balance`); numbers in `<bdi>` with `tabular-nums`.

## All cases (Yosi #15: "think of every case and show it")
Every case below gets a screen id, a demo scenario reachable from the presenter panel's "מקרים" list, and
copy in plain Hebrew (gender variants). Group in the panel exactly as here.

**Before leaving**
1. `nounderstand` — speech not understood / empty: "לא שמעתי טוב. אפשר לומר שוב, לאט." + mic + type.
2. `notfound` — place not found: "לא מצאתי את המקום. אפשר לומר שם רחוב ועיר."
3. `ambiguous` — two matches (e.g. two Clalit clinics): "יש שני מקומות כאלה. לאיזה?" two big buttons with street names.
4. `toofar` — destination > 25 km or another city with no direct line: "זה רחוק מדי לאוטובוס אחד. כדאי לבקש עזרה." + help.
5. `nodirect` — no direct line: same help offer; never suggest a transfer.
6. `tooclose` — destination < 400 m: "זה קרוב. עדיף ללכת ברגל — 5 דקות." → walking-only guidance.
7. `nightnoservice` — no bus in the next 90 min / Shabbat: "עכשיו אין אוטובוסים. האוטובוס הבא בשבת בערב בשעה 19:10." + help.
8. `noperm` — location permission refused: "בלי מיקום אני לא יכול להדריך. אפשר לבקש עזרה או לאפשר בהגדרות." (shows how, one step).

**Walking to the stop**
9. `offroute` — walking away from the route (already specced).
10. `wrongside` — at the right stop name but opposite direction: "התחנה שלך בצד השני של הכביש. לחצות במעבר החציה."
11. `gpsweak` — accuracy poor for > 30 s: "המיקום לא מדויק כרגע. כשתגיע לתחנה — לחץ 'הגעתי'." (manual mode, calm).

**At the stop**
12. `late` — bus not arrived 5 min after scheduled: "האוטובוס מתאחר. זה קורה. אפשר לחכות עוד קצת." countdown "בדרך, עוד כ־4 דקות" if realtime else "לפי לוח הזמנים".
13. `missed` — scheduled time passed by > 10 min with no boarding: "נראה שהאוטובוס עבר. הבא מגיע בעוד 12 דקות." (same line, next ride).
14. `wrongbus` — user says they boarded but GPS moves away from the route: "נראה שזה לא הקו הנכון. לרדת בתחנה הבאה, ואני אדריך משם."
15. `waitlong` — waiting > 20 min total: offer help call, and "אפשר לשבת על הספסל. אני אגיד כשהוא מגיע."

**On the bus**
16. `alert` — next stop get off (exists).
17. `passed` — passed the destination stop (exists): "אל דאגה — לרדת בתחנה הבאה."
18. `alertmissed` — alert not acknowledged within 30 s: voice repeats louder + "לחץ על הכפתור האדום באוטובוס".
19. `detour` — bus left the planned route (> 300 m): "האוטובוס נוסע בדרך אחרת. להישאר רגוע. אני עוקב."

**Anywhere**
20. `lost-*` — "איפה אני?" flow (calm → landmark → what do you see → orient) (exists).
21. `help` / `sent` — contact + copy message (Artifact) / share (phone).
22. `nocontact` — no contact saved: field to add one + public transport info line *8787.
23. `battery` — battery < 15% (Battery API where available): "הסוללה כמעט נגמרת. כדאי לשלוח לבן איפה אתה עכשיו." + help.
24. `offline` — no internet: "אין אינטרנט כרגע. אני ממשיך לפי המסלול ששמרתי." (fallback route continues).
25. `resume` — app reopened mid-journey (exists).
26. `exit` — back button / stop journey (exists).
27. `novoice` — device has no Hebrew voice: text-only notice once (exists).
28. `arrived` + `home` — arrived, take me home (exists).
