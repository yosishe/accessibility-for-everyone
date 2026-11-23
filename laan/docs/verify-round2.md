# verify-round2 — לאן? (index.html, round 2)

Verifier: independent check against `requirements-checklist.md` R1–R19, on the running app at http://localhost:8000/ (2026-11-23).
Method: Playwright pages opened with `context().newPage()` (or an isolated `browser.newContext()` for real-mode tests with mocked geolocation), at 412×915 and 360×780. `speechSynthesis.speak`, `navigator.vibrate` and `navigator.wakeLock` were stubbed and counted. No project file was edited. Scratch scripts: `/Users/26yos/at/.playwright-mcp/verifier_sweep.js`, `verifier_sweep_xl.js`. Screenshots: `/Users/26yos/at/.playwright-mcp/verifier-*.png` (contact sheet `verifier-sheet-360.png`).

**Verdict: fix.** 12 PASS · 7 PARTIAL · 0 FAIL.

## Measurement sweep (48 `?screen=` ids × 2 sizes × אתה/את = 192 renders)

My own audit, not the builder's (text nodes walked, contrast computed from computed `color` against the composited ancestor background, button rects, range line counts):

| check | 412×915 | 360×780 |
|---|---|---|
| sentence (`#say`) and body text | ≥ 32px | ≥ 32px |
| smallest text on screen | 28px step/figcap labels; **30px footer tiles "לשמוע שוב" / "איפה אני?" and quiet "הגדרות" / "לא עכשיו"**; 24px demo badge (demo only) | same |
| min contrast (normal) | 7.33 (yes/no screens), else 7.84 | same |
| min contrast (`&theme=hc`) | 16.13 | 16.13 |
| min button height | 72 | 72 |
| button labels wrapped | 0 | 0 |
| horizontal overflow / doc scroll | 0 / 0 | 0 / 0 |
| middle area scroll, default size | 0 screens | 0 screens |
| middle area scroll, `&size=xl` | 4 screens, max 18px (lost-orient) | 13 screens, max **109–112px (sent)**, 68–70px (exit) |
| primary buttons per screen | never > 1 (0 on gender, ride, planning, lost-calm, lost-ask, ambiguous, nocontact) | same |
| text broken inside a token | none | **phone number `050‑1234567` on 2 lines** on help, nodirect, battery (`.card .ds`, `overflow-wrap:break-word`) |

## R1–R19

| # | Result | Evidence |
|---|---|---|
| R1 elderly: one instruction, ≥ 32px, ≥ 7:1, one primary | **PARTIAL** | Contrast PASS (min 7.33; hc 16.13). Buttons ≥ 72 PASS. ≤ 1 primary on all 48 screens PASS. Text size fails the literal ≥ 32px: footer "איפה אני?" and "לשמוע שוב" render at **30px** on every screen, step/figcap labels at 28px. The builder's "min font 32 (micro 28)" omits the 30px footer — and "איפה אני?" is the safety button. |
| R2 Hebrew RTL, plain, gender | **PARTIAL** | `<html lang="he" dir="rtl">`, inputs `dir="auto"`. `&g=f` sweep: all user-addressed strings switch (לכי, רדי, לחצי, את רואה, בואי, כשתגיעי). Defects: contact onboarding asks "מספר הטלפון שלו:" / "איך קוראים לו?" with the example "למשל: הבת שלי רותי" (gender clash, both genders); sent-summary row hard-coded `'הולך ליעד'` (index.html:1999) shows masculine for a woman in the final walk. No string > 12 words (longest 10: passedSub). |
| R3 voice in Hebrew, unlocked by first tap | **PARTIAL** | Demo run: 37 `speak` calls, every utterance `lang=he-IL`, every screen spoken; before the first tap 0 calls (1.5 s wait), queued sentence spoken right after the tap (1.7 s). he/iw voice pick + 2 s poll + 120-char chunks in code (index.html:768–830). Not heard on a real Android phone (cannot verify here). Spoken stop line has punctuation debris: "מגיע בעוד 6 דקות , לפי לוח הזמנים, ." |
| R4 professional, SVG icons, tiers, strip, plate | **PASS** | 14 `<symbol>` icons, 0 emoji in UI (only ✓✗ inside the speech sanitizer regex, index.html:786). Three button tiers + quiet link, 4-disc journey strip, sign plate on yellow band (stop screen). Minor: confirm at 412 leaves ~100px empty above and below the card (see `verifier-desktop_demo_1_frame_1.png`). |
| R5 fits phone sizes, no scroll; desktop in phone frame | **PARTIAL** | Default size: 0 overflow / 0 scroll at 412×915 and 360×780 on all 48 ids and during both demo runs. Fails: (a) `ענק` scrolls the middle up to 112px at 360 (sent); (b) desktop 1440×900 without `?frame=1` shows a bare 640px column, frame only with `?frame=1` (iframe 374×830 centred, OK); (c) phone number wraps at 360. 393×852 not re-run by me. |
| R6 Android-ready | **PASS** (device not verified) | Real mode, isolated context: back during walk → exit "לעצור את הדרך?" → "לא — ממשיכים בדרך" returns to walk; "כן — לעצור" clears `laan.journey`. `wakeLock.request` called 1× on walk. Reload mid-journey → "להמשיך בדרך?" → walk restored. manifest (name, standalone, 192/512 PNG) + sw.js with fetch handler, all 200. Not run: Lighthouse, real device. Copy defect on resume (see defects #4). |
| R7 first entry order | **PASS** | Real mode clicked: welcome → gender (אתה/את) → home (typed, "לשמור") → confirm home → contact phone (`type=tel`) → contact name → perms → dest. |
| R8 return entry | **PASS** | After one trip + reload: "שלום שוב! לאן היום?" with `הביתה` (home icon) + recent "דיזנגוף 200"; `?screen=dest-return` shows הביתה + 2 recents. |
| R9 destination by voice or typing; Claude cleans; confirm | **PARTIAL** | Mic 156×156 on first visit (104×98 on return), field 36px, "לחפש" appears on typing, confirm yes/no works. Not verified: Claude cleaning — server reports `{"claude": false}`; the natural phrase "מרפאת כללית דיזנגוף" returned "לא מצאתי את המקום." in real mode. Confirm copy is "זה המקום?" + card, not "הבנתי: X. נכון?" (spoken "X. זה המקום?") — meaning kept. |
| R10 direct line, walking map, "walk X m to stop Y" | **PASS** | Real `/api/plan` (live server): line 2, "לכי לתחנה דיזנגוף סנטר / דיזנגוף." + "200 מטר כ־3 דקות" + Leaflet map with route. Demo: "לך לתחנה דיזנגוף / קינג ג'ורג'." + "250 מטר". Planning sub "רק אוטובוס ישיר, בלי החלפות." |
| R11 stop / ride / alert | **PASS** | Stop: "עולים על קו 5" + plate + "בעוד 5 דקות / לפי לוח הזמנים"; spoken "מגיע בעוד 6 דקות". Ride: figure "עוד 3 תחנות", spoken "נשארו N תחנות" at each stop. Alert: full-screen #FFD400/black, 56px "יורדים בתחנה הבאה!", 1 Hz inverse flash, voice every 5 s, `vibrate([500,200,500,200,500])` logged at 58.8 s. After 30 s "לחצי על הכפתור האדום באוטובוס!" added. |
| R12 "הגעת!" + "קח אותי הביתה" | **PASS** | Demo: arrived → `b-home` "קח אותי הביתה" → confirm "הבית" → walk to new stop within 7 s. |
| R13 settings small, at bottom | **PASS** | Quiet "הגדרות" link (30px, underlined) under the footer, on the destination screen only. |
| R14 "איפה אני?" flow | **PARTIAL** | Clicked at 360, `&g=f`: calm "הכל בסדר. אני איתך. בואי נבדוק יחד." → auto-advance (≤ 3.9 s) → "את רואה את סופר־פארם דיזנגוף?" → לא → "ואולי את רואה את בנק לאומי?" → לא → "מה את רואה לידך?" → typed "סופר פארם" → "את ליד סופר־פארם דיזנגוף." + **"התחנה 100 מטר קדימה."** The final instruction has no direction a lost person can act on ("קדימה" relative to what?). |
| R15 send location + call | **PASS** (device not verified) | Help: "לשלוח איפה אני" (primary) + "להתקשר לרותי"; `tel:` / `sms:` / `navigator.share` in code (index.html:2006–2015). Demo skips the share sheet. |
| R16 "sent" summary | **PASS** | "שלחתי לרותי איפה את." + rows "ליד סופר־פארם / בדרך למרפאת כללית / קו 5, בעוד 6 דקות", also spoken. Minor: "שלחתי" is claimed when the share sheet resolves (the user may not have pressed send in WhatsApp); finalwalk row is masculine (R2). |
| R17 wrong direction → "צריך עזרה?" | **PASS** | `&lost=1&auto=1`: prompt "נראה שהתרחקת מהדרך. לעזור לך?" at **18.3 s** (412, `&g=f`) and 18.5 s (360), one vibration 200 ms, then back to walk and stop at 33.8 s. |
| R18 28 cases | **PARTIAL** | 27 present and correct, 1 partial (nocontact: no *8787 line). Table below. |
| R19 demo ≤ 90 s; fallback on API failure | **PASS** | `?demo=1&auto=1`, one click at 0.4 s: "הגעת!" at **74.6 s** (412) and **74.6 s** (360). Order: dest 0.4 → confirm 2.7 → planning 5.7 → walk 6.7 → stop 19.1 → ride 28.9 → alert 59.0 → ride 62.7 → off 64.8 → finalwalk 67.5 → arrived 74.6. localStorage empty after the run; only `sessionStorage['laan.demo.journey']`. `/api/**` aborted in real mode → confirm 3.5 s → walk 4.6 s on the fallback route. But see defect #1: the fallback also replaces the user's real destination. |

## The 28 cases (R18)

| # | id | Result | What the screen shows (412, אתה) |
|---|---|---|---|
| 1 | nounderstand | PASS | "לא שמעתי טוב." / "אפשר לומר שוב, לאט, או לכתוב כאן." + mic + field |
| 2 | notfound | PASS | "לא מצאתי את המקום." / "אפשר לומר שם רחוב ועיר." (also reached for real) |
| 3 | ambiguous | PASS (screen only) | "יש שני מקומות כאלה. לאיזה?" + 2 buttons with streets; not wired to a real trigger |
| 4 | toofar | PASS | "זה רחוק מדי לאוטובוס אחד." / "כדאי לבקש עזרה." |
| 5 | nodirect | PASS | "אין אוטובוס ישיר לשם." / "אפשר לבקש עזרה מרותי." — no transfer offered; phone wraps at 360 |
| 6 | tooclose | PASS | "זה קרוב. עדיף ללכת ברגל." + "200 מטר כ־3 דקות הליכה" |
| 7 | nightnoservice | PASS | "עכשיו אין אוטובוסים." + "19:10" / "האוטובוס הבא, בשבת בערב" |
| 8 | noperm | PASS | "בלי מיקום אני לא יכול להדריך." + "הגדרות הטלפון ← מיקום ← להפעיל" |
| 9 | offroute | PASS | "נראה שהתרחקת מהדרך. לעזור לך?" (also triggered live at 18.3 s) |
| 10 | wrongside | PASS (screen only) | "התחנה שלך בצד השני של הכביש." / "לחצות במעבר החציה, בזהירות." |
| 11 | gpsweak | PASS | "המיקום לא מדויק כרגע." / 'כשתגיע לתחנה — לחץ "הגעתי לתחנה".' — the "הגעתי לתחנה" button exists on the walking screen (index.html:1422) |
| 12 | late | PASS | "האוטובוס מתאחר. זה קורה." / "אפשר לחכות עוד קצת." + countdown "לפי לוח הזמנים" |
| 13 | missed | PASS | "נראה שהאוטובוס עבר." + "הבא בעוד 12 דקות" / "אותו קו, אותה תחנה" |
| 14 | wrongbus | PASS | "נראה שזה לא הקו הנכון." / "רד בתחנה הבאה, ואני אדריך משם." |
| 15 | waitlong | PASS | "אפשר לשבת על הספסל." / "אני אגיד כשהאוטובוס מגיע." + call button |
| 16 | alert | PASS | full-screen flashing alert (see R11) |
| 17 | passed | PASS | "נראה שעברת את התחנה." / "אל דאגה — רד בתחנה הבאה, ואני אדריך אותך בחזרה." |
| 18 | alertmissed | PASS | alert + "לחץ/לחצי על הכפתור האדום באוטובוס!", voice every 5 s |
| 19 | detour | PASS | "האוטובוס נוסע בדרך אחרת." / "להישאר רגועים. אני עוקב אחרי הדרך." |
| 20 | lost-* | PASS | calm / landmark / ask / orient (see R14 for the "קדימה" issue) |
| 21 | help / sent | PASS | see R15/R16 |
| 22 | nocontact | **PARTIAL** | "למי להתקשר?" + phone field + "להתקשר למוקד". The *8787 line from the spec is never shown: `hotlineSub` (index.html:651) is defined and unused; the button does not say which number it dials |
| 23 | battery | PASS | "הסוללה כמעט נגמרת." / "כדאי לשלוח לרותי איפה אתה." |
| 24 | offline | PASS | "אין אינטרנט כרגע." / "אני ממשיך לפי המסלול ששמרתי." |
| 25 | resume | PASS (copy defect) | "להמשיך בדרך?" + card; real mode shows "באמצע הנסיעה בקו 2" while still walking to the stop |
| 26 | exit | PASS | "לעצור את הדרך?" — also reached with the real back button |
| 27 | novoice | PASS | notice "הטלפון לא יודע לדבר עברית, אז ההוראות יופיעו בכתב." 32px, visible |
| 28 | arrived + home | PASS | "הגעת!" + "קח אותי הביתה" (works end to end in demo) |

## Top defects, ranked by harm to an older user

1. **Real mode silently swaps the user's destination (and home) for the demo clinic when the server is unreachable.** index.html:1276 (`if (noServer()) return … FALLBACK.dest`) and :1281 (geocode error → `FALLBACK.dest`). Reproduced: real mode, `/api/**` aborted, typed "בית החולים איכילוב" → confirm "מרפאת כללית, דיזנגוף · כ־1.5 קילומטר מכאן". On GitHub Pages (no server) every real user is routed there; the same resolver serves the home address during onboarding. With a host `understand` result the card even shows the right *name* on the clinic's *coordinates*. Screen: confirm. Fix: use `FALLBACK` only when `DEMO`; in real mode with no server show notfound/"אין חיבור כרגע" and offer help.
2. **"איפה אני?" ends with a directionless instruction.** lost-orient: "התחנה 100 מטר קדימה." A lost person has no "forward". Fix: anchor to the confirmed landmark and a street ("התחנה ברחוב דיזנגוף, 100 מטר מסופר־פארם — ללכת לכיוון בנק לאומי"), or show the map arrow and say "ללכת לכיוון החץ".
3. **Contact phone number breaks across two lines at 360px** ("050‑123456" / "7") on help, nodirect, battery. Misreading or misdialling risk. Fix: `.card .ds.tel{ white-space:nowrap; direction:ltr; unicode-bidi:isolate; }` and shrink to fit (`font-size:min(32px, 8.5vw)`), or drop the icon column on narrow screens.
4. **Resume says "באמצע הנסיעה בקו 2" when the person has not boarded.** resume, index.html:1605. Fix: caption by step — walk "בדרך לתחנה X", stop "בתחנה X", ride "באוטובוס קו N", finalwalk "בדרך ל־Y". Also "לא" deletes the journey in one tap; ask once ("לעצור את הדרך?").
5. **Permissions copy points to a button that likely does not exist.** perms: 'עכשיו הטלפון ישאל — לחץ "אפשר".' The Android Chrome prompt offers "while visiting the site / this time / don't allow" options, no "אפשר" (not checked on a device). Fix: "עכשיו הטלפון ישאל. לחץ על הכפתור שמאשר" or name the real label after checking on a Hebrew Android phone.
6. **The help button text is 30px, below the ≥ 32px rule** (footer "איפה אני?" and "לשמוע שוב", every screen; step labels 28px). Fix: 32px in the footer tiles (they are 88px tall and have room), keep 28px only if Yosi accepts micro labels as an exception.
7. **nocontact never shows *8787.** `hotlineSub` unused; button "להתקשר למוקד" does not say which line. Fix: show `t('hotlineSub')` as the sub, or label the button "להתקשר למוקד *8787".
8. **Gender copy errors.** contact: "מספר הטלפון שלו:" / "איך קוראים לו?" next to the example "הבת שלי רותי" → "מה המספר?" / "מה השם?". sent (finalwalk): `'הולך ליעד'` (index.html:1999) → `g('הולך ליעד','הולכת ליעד')` or neutral "בדרך ליעד ברגל".
9. **`ענק` text size scrolls the middle area** at 360×780 on 13 screens (sent 112px, exit 70px, wrongside 30px). The primary button stays visible, but the sent summary and the exit card are cut. Fix: at ≤ 800px tall in `ענק`, hide the map/secondary card or drop the sub line.
10. **Desktop frame needs `?frame=1`.** Plain desktop = a 640px column. Fix: auto-frame when `innerWidth > 600 && matchMedia('(pointer:fine)')`, keep `?frame=0` to opt out.

Lower: spoken stop line has stray commas ("… 6 דקות , לפי לוח הזמנים, ."; clean in `forSpeech`); no `prefers-reduced-motion` override for the 1 Hz full-screen flash; "לחכות לבא" reads awkwardly ("לחכות לאוטובוס הבא"); back on the destination screen never lets the user leave the app.

## Builder claims checked

| claim (implementer-round2.md) | result |
|---|---|
| demo "הגעת!" at 74.5 s, both sizes | confirmed: 74.6 s / 74.6 s |
| off-route prompt 18.3 s with `&lost=1&g=f` | confirmed: 18.3 s |
| min font 32 (micro 28) | **inaccurate**: 30px footer and quiet buttons on every screen |
| min contrast 7.33, 0 failures at 412/360 | confirmed |
| localStorage empty during demo | confirmed |
| resume after reload | confirmed (copy defect #4) |
| fallback with `/api` blocked | confirmed, but it also replaces real destinations (defect #1) |
| ענק scroll max 112px at 360 | confirmed (109–112px) |

## Not checked
- A real Android phone: TTS voice, vibration, wake lock, share sheet, `tel:`/`sms:`, permission prompt labels, back button, keyboard overlap.
- Claude destination cleaning (server has no key: `/api/health` → `{"ok": true, "claude": false}`).
- Lighthouse installability; 393×852 and 390×844 (builder ran them).
