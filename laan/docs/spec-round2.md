# לאן? — round 2 spec: "I'm not sure where I am" + elderly UX refinements

Applies to /Users/26yos/at/laan/index.html and /Users/26yos/at/laan/server.py. Keep everything in spec-ui.md
unless overridden here.

## A. "אני לא בטוח איפה אני" — a short guided conversation, not one sentence

Why: a lost older person needs (1) to be calmed first, (2) confirmation that the app's idea of their location
matches what they see — GPS in a city is often 30–80 m off and a wrong "you are at X" makes things worse,
(3) one next step. Never more than one question per screen; every answer is a big button or the microphone.

Flow (each line = one screen, spoken aloud, footer still present):

1. **Calm** — "הכל בסדר. אני איתך. בוא נבדוק יחד." (auto-advances after the sentence is spoken — the only
   auto-advance besides demo; ≤ 3 s) Meanwhile: get a fresh GPS fix (`getCurrentPosition`, 8 s timeout,
   high accuracy) + `/api/reverse` + `/api/nearby` (see C).
2. **Confirm with a landmark** — pick the single most visible nearby thing (priority: the bus stop of the
   current journey if ≤ 80 m, then a named landmark from /api/nearby: pharmacy, bank, supermarket, clinic,
   school, synagogue, park, big shop; else the street + nearest crossing street).
   Ask: "אתה רואה לידך <landmark>?" — e.g. "אתה רואה לידך את בית המרקחת סופר־פארם?"
   Buttons: "כן, אני רואה ✓" (green) / "לא ✗" (red).
   - כן → step 4 (location confirmed).
   - לא → try the next landmark once ("ואולי אתה רואה <landmark2>?"). Second לא → step 3.
3. **Ask what they see** — "מה אתה רואה לידך? תגיד שם של חנות, רחוב או שלט." Big microphone + text field.
   Send `{lat, lon, accuracy, seen: <text>, candidates: [nearby names], step, route}` to `/api/where-am-i`;
   Claude matches the description to the candidates and returns one calm sentence + optional corrected
   position. If nothing matches: "לא הצלחתי לזהות. בוא נתקשר ל־<contact>." → step 5 directly.
4. **Orient + one action** — one sentence with where they are relative to the journey and what to do:
   - walking: "אתה ברחוב דיזנגוף, ליד סופר־פארם. התחנה נמצאת 100 מטר קדימה." + map with them and the stop.
   - at stop: "אתה בתחנה הנכונה. קו 5 מגיע בעוד 4 דקות."
   - riding: "אתה באוטובוס הנכון. נשארו 3 תחנות."
   - wrong way / far (> 300 m off the walking path, or riding past the destination): "זה בסדר. בוא נחפש
     דרך חדשה מכאן." → re-plan from here.
   Buttons: "הבנתי, ממשיכים" (primary) and "📞 צריך עזרה" (secondary → step 5).
5. **Help from a person** (also reachable from the footer when no journey is active) — "בוא נקרא ל־<contact name>."
   Two big buttons:
   - "📍 שלח לו איפה אני" → `navigator.share({text})` with "אני כאן: <street>, ליד <landmark>. https://maps.google.com/?q=<lat>,<lon>"
     (WhatsApp/SMS sheet on Android). Fallback when share is unavailable: `sms:<phone>?body=...`.
   - "📞 התקשר ל־<contact name>" → `tel:<phone>`.
   If no contact saved: show the phone field right there ("למי להתקשר?") with "שמור והתקשר", and a
   secondary "📞 מוקד התחבורה הציבורית" → `tel:*8787`. Do not offer emergency numbers for being lost.
   Sending the location never happens without the user pressing the button.

Gender variants for all strings (לך/ראית/רואה ↔ רואָה etc.).

Server changes:
- `GET /api/nearby?lat=&lon=` → Overpass API (`https://overpass-api.de/api/interpreter`, 6 s timeout) for
  named `amenity|shop|tourism|leisure=park` within 120 m, plus bus stops; return up to 8 `{name, kind_he, dist}`
  sorted by visibility priority then distance. `ok:false` on failure → client uses street + cross-street only.
- `/api/where-am-i` accepts `seen` and `candidates`; Claude prompt: decide which candidate the person most likely
  sees, answer ONE calm Hebrew sentence ≤ 14 words, JSON `{"text": "...", "match": "<candidate name or null>"}`.
- Local fallback when Claude fails: if `seen` fuzzy-matches a candidate (substring after removing ה־/ניקוד),
  build the sentence locally.

Demo: the help flow works in demo with canned nearby = ["סופר־פארם דיזנגוף" (pharmacy, 25 m), "בנק לאומי" (bank, 40 m), "כיכר דיזנגוף" (square, 90 m)].

## B. Elderly UX refinements (from walking through the app)

1. **Footer:** "🔊 תקרא שוב" and "😕 אני לא בטוח איפה אני" stay; settings is NOT a main-screen button.
   Move "הגדרות" to a small (but still ≥ 56px tall, 28px text) text button at the very bottom of the
   destination screen only, under the footer, so it is never confused with the main action.
2. **Returning entry should feel known:** destination screen on a returning visit shows
   "שלום שוב! לאן היום?" and, above the microphone, up to 3 big shortcut buttons: "🏠 הביתה" (if home saved)
   + the 2 most recent destinations (store `recent` in settings). One tap → confirm screen → plan.
   The first visit shows only the microphone and text field.
3. **Home screen during onboarding** needs a visible primary "שמור" button after something is typed/spoken
   (today only "לא עכשיו" is visible). Same for the contact screen ("שמור"), and ask for the contact's name too
   ("איך קוראים לו?" — e.g. "הבת שלי רותי"), used in "התקשר לרותי".
4. **Resume after interruption** must work: verify that a saved journey with step walk/stop/ride shows
   "להמשיך את הדרך ל־<dest>?" on reload.
5. Footer label "אני לא בטוח איפה אני" → shorter and warmer: "😟 הלכתי לאיבוד?" is too negative; use
   "🧭 איפה אני?" (fits one line at 32px on 360 px wide screens).
6. Text field placeholder "או כתוב כאן" → "או לכתוב כאן" (infinitive, gender-neutral). Prefer infinitive
   phrasing for button labels everywhere it avoids gender ("לחזור", "להתקשר").

## C. Message #8 — sent-confirmation with a journey summary, and proactive off-route help

1. **What is sent to the contact** (via `navigator.share`, fallback `sms:`) is a short summary the son can act on,
   not just a pin. Example (gender of the user applied):
   "אני כאן: רחוב דיזנגוף, ליד סופר־פארם. https://maps.google.com/?q=LAT,LON
    אני בדרך ל: מרפאת כללית, דיזנגוף.
    כדאי לי לקחת: קו 5 מתחנת 'דיזנגוף/קינג ג'ורג'' (100 מטר ממני), עוד 4 דקות, לרדת אחרי 5 תחנות.
    (נשלח מהאפליקציה 'לאן?')"
   When there is no active journey, the "בדרך ל" and "כדאי לקחת" lines are omitted.
2. **Sent screen** — after `navigator.share()` resolves (or after the SMS app was opened):
   big ✓ and "שלחתי ל־<contact name> איפה אתה." and below it, at 32px, the same three-line summary in plain
   words ("אתה ליד סופר־פארם · בדרך למרפאה · כדאי לקחת קו 5") so the user sees exactly what was sent.
   Primary: "📞 להתקשר ל־<contact name>"; secondary: "לחזור לדרך". Honest wording: a web app cannot know that
   WhatsApp delivered the message, so if share was cancelled (AbortError) say nothing was sent and offer again.
3. **Off-route detection** (walk and finalwalk steps, real and demo): every GPS fix, compute distance to the
   walking polyline and distance to the target. Trigger when, for ≥ 45 s (or 3 consecutive good fixes):
   distance to path > 60 m, OR distance to target grew by > 40 m since the closest point reached.
   Then a gentle full-screen prompt (not the flashing alert): "נראה שהתרחקת מהדרך. צריך עזרה?"
   with "כן, אני צריך עזרה" (→ section A step 2, landmark confirmation, then re-plan) and
   "לא, אני בסדר" (silence the check for 3 minutes). Spoken once plus one short vibration; never repeats more
   often than every 3 minutes. Riding: if GPS passes the destination stop by > 1 stop → "נראה שעברת את התחנה…" (existing).
   Demo: add `&lost=1` — the simulator walks 120 m off the path midway so the prompt can be shown indoors.
