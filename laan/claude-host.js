/* claude-host.js - lets the "לאן?" app run as a Claude-hosted Artifact with no server.
 *
 * Does nothing (window.LaanHost stays undefined) unless window.claude.use exists.
 * Inside an Artifact it exposes:
 *   window.LaanHostReady  Promise resolving to window.LaanHost once capabilities have resolved
 *   window.LaanHost = {
 *     noServer: true,
 *     understand(text, city)  -> Promise<{query, display_name}|null>      (sample.json, "quick")
 *     whereAmI({lat,lon,street,step,route,gender,seen,candidates})
 *                             -> Promise<{text, match}|null>              (sample.json, "quick")
 *     dictation: null | { start(onFinal(fullText), onState("listening"|"idle")), stop() }
 *     speak(text)             -> Promise<boolean>   (false: caller falls back to speechSynthesis)
 *   }
 * Every method returns null/false when a capability is absent or refused; none throws.
 * After rate_limited / not_granted / similar a capability is switched off for this page load
 * and never called again (no retries). Results are plain strings: the app must use textContent.
 */
(function () {
  "use strict";
  var W = typeof window !== "undefined" ? window : null;
  if (!W || !W.claude || typeof W.claude.use !== "function") return;

  var off = { sample: false, tts: false, dictation: false };
  var S = null, T = null, D = null;
  var STOP = { rate_limited: 1, not_granted: 1, sampling_disabled: 1, not_declared: 1,
               capability_disabled: 1, capability_removed: 1, session_expired: 1 };

  function use(name) {
    try { return Promise.resolve(W.claude.use(name)).catch(function () { return null; }); }
    catch (e) { return Promise.resolve(null); }
  }
  function str(v) { return typeof v === "string" ? v.trim() : ""; }
  function fail(cap, e) { if (e && STOP[e.code]) off[cap] = true; return null; }

  var DEST = "You turn an elderly Israeli's spoken Hebrew into a place search. " +
    "Strip filler such as 'אני צריך להגיע ל', 'בבקשה', 'תביא אותי'. Expand common phrasings " +
    "(e.g. 'קופת חולים בדיזנגוף' means a health clinic on Dizengoff street). If no city is " +
    "mentioned, use the city given to you. Reply with JSON only: " +
    '{"query": "<Hebrew query for Nominatim, street and city>", ' +
    '"display_name": "<short Hebrew name, max 6 words, to read aloud>"}';

  var WHERE = "You calm and orient an elderly person who feels lost on a bus journey in Israel. " +
    "Answer in ONE Hebrew sentence of at most 14 simple words: where they are and what to do " +
    "next. No questions, no apologies, no technical words, no English. Use the grammatical " +
    "gender given to you. Reply with JSON only: " +
    '{"text": "<the sentence>", "match": null}';

  var MATCH = "You help an elderly person who feels lost on a bus journey in Israel. You get a list of " +
    "named places near them and what they say they see. Decide which candidate they most likely " +
    "see (spelling, spacing and hyphens may differ; they may be speaking from memory). Answer ONE " +
    "calm Hebrew sentence of at most 14 simple words telling them where they are, next to that " +
    "place. No questions, no apologies, no English. Use the grammatical gender given to you. " +
    "Reply with JSON only: " +
    '{"text": "<the sentence>", "match": "<the candidate name exactly as given, or null>"}';

  function understand(text, city) {
    text = str(text);
    if (!S || off.sample || !text) return Promise.resolve(null);
    var p = DEST + "\n\nCity: " + (str(city) || "תל אביב") + "\nSpeech: " + text;
    return S.json(p, { modelTier: "quick" }).then(function (o) {
      var q = o && str(o.query);
      return q ? { query: q, display_name: str(o.display_name) || q } : null;
    }, function (e) { return fail("sample", e); }).catch(function () { return null; });
  }

  function whereAmI(b) {
    b = b || {};
    if (!S || off.sample) return Promise.resolve(null);
    var g = b.gender === "f" ? "f" : "m";
    var seen = str(b.seen);
    var cands = (Array.isArray(b.candidates) ? b.candidates : [])
      .map(String).filter(function (c) { return c.trim(); }).slice(0, 12);
    var p = (seen ? MATCH : WHERE) + "\n\nGender: " + g + "\nLocation: " + b.lat + ", " + b.lon +
      "\nNearest street: " + (b.street || "") + "\nCurrent step: " + (b.step || "") +
      "\nRoute: " + (b.route || "");
    if (seen) p += "\nCandidates: " + JSON.stringify(cands) + "\nThe person says they see: " + seen;
    try {
      return S.json(p, { modelTier: "quick", cache: false }).then(function (o) {
        var t = o && str(o.text).replace(/^"+|"+$/g, "");
        if (!t) return null;
        return { text: t, match: seen && cands.indexOf(o.match) >= 0 ? o.match : null };
      }, function (e) { return fail("sample", e); }).catch(function () { return null; });
    } catch (e) { return Promise.resolve(null); }
  }

  var muted = false;
  function speak(text) {
    text = str(text);
    if (muted) return Promise.resolve(true);   // viewer turned the voice off: respect it, stay silent
    if (!T || off.tts || !text) return Promise.resolve(false);
    try {
      return Promise.resolve(T.speak(text, { language: "he", rate: 0.85 })).then(
        function () { return true; },
        function (e) { fail("tts", e); if (e && e.code === "not_granted") { muted = true; return true; } return false; });
    } catch (e) { return Promise.resolve(false); }
  }

  var subs = [];
  function unsub() { subs.forEach(function (u) { try { u(); } catch (e) {} }); subs = []; }

  // Called synchronously from the click handler: nothing is awaited before D.start().
  var dictation = {
    start: function (onFinal, onState) {
      if (!D || off.dictation) { if (onState) try { onState("idle"); } catch (e) {} return; }
      var full = "";
      function emit(fn, a) { if (typeof fn === "function") try { fn(a); } catch (e) {} }
      try {
        unsub();
        subs.push(D.onFinal(function (e) {
          full = (full + (e && typeof e.text === "string" ? e.text : "")).trim();
          if (full) emit(onFinal, full);
        }));
        subs.push(D.onState(function (e) {
          var s = e && e.state;
          if (s === "listening") emit(onState, "listening");
          else if (s === "idle") {
            if (e.reason === "not_granted" || e.reason === "unavailable" || e.reason === "rate_limited") off.dictation = true;
            emit(onState, "idle");
          }
        }));
        D.start({ language: "he" }).catch(function (e) {
          if (e && (e.code === "not_granted" || e.code === "unavailable" || e.code === "rate_limited")) off.dictation = true;
          emit(onState, "idle");
        });
      } catch (e) { emit(onState, "idle"); }
    },
    stop: function () {
      try { if (D) return Promise.resolve(D.stop()).catch(function () {}); } catch (e) {}
      return Promise.resolve();
    }
  };

  var host = { noServer: true, understand: understand, whereAmI: whereAmI, dictation: null, speak: speak };
  W.LaanHost = host;
  W.LaanHostReady = (async function () {
    try {
      var r = await Promise.all([use("sample"), use("tts"), use("dictation")]);
      S = r[0] && typeof r[0].json === "function" ? r[0] : null;
      T = r[1] && typeof r[1].speak === "function" ? r[1] : null;
      D = r[2] && typeof r[2].start === "function" ? r[2] : null;
      host.dictation = D ? dictation : null;
    } catch (e) {}
    return host;
  })();
})();
