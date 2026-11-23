# implementer-fixes — לאן? index.html, after verify-round2

Files changed: `/Users/26yos/at/laan/index.html`, `/Users/26yos/at/laan/mockup.html` (one new entry: `noplaces`).
Not touched: artifact/laan.html, server.py, sw.js, manifest.json, claude-host.js.
Backups of the pre-fix files: scratchpad `index.before.html`, `mockup.before.html`.
Audit scripts: `/Users/26yos/at/.playwright-mcp/impl_sweep.js`, `impl_sweep_xl.js`, `impl_flows.js`. Screenshots: `/Users/26yos/at/.playwright-mcp/impl-*.png`.

## Defect → fix → evidence

| # | defect (verify-round2) | fix | evidence |
|---|---|---|---|
| 1 | Real mode swapped the typed destination (and home) for the demo clinic when there was no server / geocode failed | `resolvePlace`: `FALLBACK.dest` only when `DEMO`. Real mode + `noServer()` or geocode error → `{status:'nolookup'}` → new screen `noplaces`. Copy: say "עכשיו אני לא יכול למצוא מקומות בלי אינטרנט." (8 words); sub "אתה יכול / את יכולה לבקש עזרה מרותי." (or "…להתקשר למוקד לעזרה." with no contact); buttons: call contact (or מוקד *8787) + "לנסות שוב". Home mode: sub "אתה יכול / את יכולה לשמור את הבית אחר כך.", buttons "להמשיך" (→ homeSkip, nothing saved) + "לנסות שוב". Also: real-mode plan fallback (Dizengoff line 5) only when origin and destination are both within 500 m of that route, else `noplaces` with "עכשיו אני לא יכול לחפש אוטובוס בלי אינטרנט."; no GPS fix → new `nofix` screen instead of planning from Dizengoff; "איפה אני?" and the share message no longer use `FALLBACK.start` as a fake position in real mode | Real mode, `/api/**` aborted, typed "בית החולים איכילוב" → screen `noplaces`, buttons [להתקשר לרותי, לנסות שוב]. Onboarding home "הרצל 5, חולון" → `noplaces` → "להמשיך" → `contact`, `settings.home === null`. Screenshot impl-noserver-dest.png |
| 2 | lost-orient "התחנה 100 מטר קדימה." — no direction | `towardRef()`: a nearby place within 45° of the bearing to the stop, else the stop's cross street ("רחוב קינג ג'ורג'"). Sub: "התחנה N מטר מכאן. ללכת לכיוון X." Map shows "את/אתה" + "התחנה" (path from current position). Demo nearby places got approximate coordinates. 360 map min-height 110px on this screen only | 360 `&g=f`: "את ליד סופר־פארם דיזנגוף." / "התחנה 150 מטר מכאן. ללכת לכיוון כיכר דיזנגוף." + map with both labels (impl-lost-orient-360.png) |
| 3 | Phone number wrapped at 360 | `telHTML()` → `<bdi dir="ltr" class="tel">` with nowrap, 32px fixed; contact card built with a separate number row; ≤380px: initial disc 48px, card gap 12px. Used on help, nodirect, battery, nocontact, noplaces | Sweep: every visible `.tel` on 1 line at 32px, 412 and 360, both genders, both sizes (impl-help-360.png) |
| 4 | Resume said "באמצע הנסיעה בקו 2" while walking | `resumeWhere()`: walk "בדרך לתחנה X" · stop "בתחנה X, קו N" · ride/passed "באוטובוס, קו N" · finalwalk "בדרך ליעד, ברגל". "לא" now opens "לעצור את הדרך?" (keep → resumes the step) instead of deleting the journey | `?screen=resume-walk` → "בדרך לתחנה דיזנגוף / קינג ג'ורג'"; `?screen=resume` → "באוטובוס, קו 5" |
| 5 | Footer tiles and quiet links 30px; no single exception list | `.tile` and `.b-quiet` 32px (tile letter-spacing −0.01em, ≤380px tile padding 4px, gap 10px); `micro` class removed from tiles. One comment above `.step` lists the only five sub-32px exceptions (step label 28, figcap 28, band "לכיוון" 28, demo badge 24, map licence 11) | Sweep: 0 non-exception text < 32px in 204 renders; tile/quiet font 32 everywhere; 0 wrapped buttons |
| 6 | nocontact had no *8787 | Line under the field: "אפשר גם להתקשר למוקד *8787." (number isolated LTR); spoken too. nodirect without a contact shows a hotline card | impl-nocontact-360.png; star renders left of digits (measured glyph x) |
| 7 | Gender: contact onboarding "שלו / לו"; sent row "הולך ליעד" | "אפשר לכתוב כאן מספר טלפון." / "מה השם?"; `walkingDest` = g('הולך ליעד','הולכת ליעד') | shareInfo finalwalk `&g=f` → "הולכת ליעד"; contact sub neutral |
| 8a | R3 spoken stop line "6 דקות , לפי לוח הזמנים, ." | `forSpeech`: "(x)" → ", x", spaces before punctuation and ",." removed | Demo speech: "מגיע בעוד 6 דקות, לפי לוח הזמנים." |
| 8b | R5 `ענק` scrolled up to 112px at 360 | `fitText()`: in ענק, `--s` steps 1.2 → 1.0 until `#main` fits (reading text never below 32px); runs on render, setSay, setButtons, resize, novoice notice | xl sweep 204 renders: 0 main scroll, 0 failures |
| 8c | R5 desktop frame needed `?frame=1` | Auto phone frame when width > 600 and `pointer: fine`; `?frame=0` opts out | 1440×900: plain and `?demo=1` framed, `?frame=0` not framed |
| 8d | perms pointed to an "אפשר" button that may not exist | "עכשיו הטלפון ישאל. לחץ/לחצי על הכפתור שמאשר." | copy |
| 8e | "לחכות לבא" | "לחכות לאוטובוס הבא" | sweep: no wrap at 360 |

## Checks run (2026-11-23, live server http://localhost:8000, Playwright via `page.context().newPage()`)
- Default size: 51 ids (48 old + noplaces, noplaces-home, resume-walk) × 412×915/360×780 × אתה/את = 204 renders → **0 failures** (min font ≥ 32 outside the exception list, contrast ≥ 7, buttons ≥ 72, no wrap, ≤ 1 primary, no horizontal/doc/middle scroll, phone numbers one line, tiles 32).
- `&size=xl`: 204 renders → **0 failures** (after fitText).
- 28 case ids + new ids render with 0 page errors.
- `?demo=1&auto=1`: "הגעת!" at **72.6 s** (412×915) and **72.7 s** (360×780).
- No-server typed destination and home: see rows 1.

## Not checked / open
- Real Android phone (voice, vibration, share sheet, permission prompt wording).
- Claude cleaning of free speech (server has no key).
- "שלחתי" is still claimed when the share sheet resolves (R16 minor, unchanged).
