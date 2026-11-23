# לאן? — every requirement Yosi asked for (the acceptance checklist)

Each line is checked by the verifier on the finished app at phone size (412×915 and 360×780). Source = Yosi's message.

## Audience and look
- [ ] R1 Built for elderly people: one instruction per screen, huge text (≥ 32px), high contrast (≥ 7:1), one primary button per screen. (brief)
- [ ] R2 Hebrew RTL throughout, plain simple Hebrew, gender variants (אתה/את). (brief, #2)
- [ ] R3 Every instruction is also read aloud in Hebrew; the voice really works on Android Chrome (first tap unlocks it). (brief, #12)
- [ ] R4 Clear, big and simple, yet professional — does not look generated: real SVG icons (no emoji), distinct button tiers, journey strip, bus-sign plate, no empty middle. (#9, #13, #16)
- [ ] R5 Fitted to and shown at phone size: fills 360×780 / 393×852 / 412×915 exactly with no scrolling; on desktop shown inside a phone frame. (#12, #14, #20)
- [ ] R6 Android-ready: installable, back button handled, screen stays awake, journey survives interruption. (#1)

## Flow
- [ ] R7 First entry: welcome → אתה/את → home → contact (name + phone) → permissions explained. (#5)
- [ ] R8 Return entry is more advanced: "שלום שוב! לאן היום?", 🏠 home shortcut, two recent destinations. (#5)
- [ ] R9 Destination by voice (big mic) or typing; Claude cleans the free speech; confirm screen "הבנתי: X. נכון?" כן/לא. (brief)
- [ ] R10 Direct bus line only (no transfers), walking route to the stop on a map, "walk X m to stop Y". (brief)
- [ ] R11 At the stop: "עלה על קו N, מגיע בעוד M דקות". On the bus: "נשארו K תחנות", then a flashing full-screen alert with voice + vibration "בתחנה הבאה יורדים!". (brief)
- [ ] R12 "הגעת!" + "קח אותי הביתה". (brief)
- [ ] R13 Settings at the bottom, small, never confused with the main action. (#7)

## "Where am I?" and help
- [ ] R14 "איפה אני?" detects location, confirms with a visible landmark ("אתה רואה לידך X?"), then asks "מה אתה רואה לידך?" if not, then gives one calm instruction. (#6)
- [ ] R15 Option to send the location to a contact and to call them. (#7)
- [ ] R16 After sending, the app shows that the location was sent to the son, with a summary: where she is, where she said she wants to go, and which bus to take. (#8)
- [ ] R17 Detects walking in the wrong direction / growing distance to the target and asks "צריך עזרה?". (#8)

## Cases
- [ ] R18 All 28 cases from spec-artifact.md "All cases" exist as screens with plain-Hebrew copy, each reachable for demonstration. (#15)

## Delivery
- [ ] R19 Demo mode `?demo=1` (and `&auto=1`) runs the whole journey in ≤ 90 s indoors; fallback Tel Aviv route when any API fails. (brief)
- [ ] R20 Claude-hosted Artifact version (sample/dictation/tts), phone-sized, with presenter panel. (#10, #11, #13)
- [ ] R21 Public GitHub repo "accessibility-for-everyone" + GitHub Pages live demo, kept up to date. (#17, #18) — done for v1
