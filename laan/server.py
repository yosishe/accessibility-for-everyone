#!/usr/bin/env python3
"""לאן? — tiny stdlib-only server.

Serves the static app and proxies every external call so the browser talks only
to this origin: no CORS, the Anthropic key never reaches the client, and every
upstream failure becomes a quiet {"ok": false} that the app answers with its
hard-coded fallback route.
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.environ.get("PORT", "8000"))
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "").strip()
MODEL = "claude-fable-5-2"
UA = "laan-bus-guide/1.0 (accessibility demo; stdlib urllib)"
TIMEOUT = 6

NOMINATIM = "https://nominatim.openstreetmap.org"
STRIDE = "https://open-bus-stride-api.hasadna.org.il"
OSRM = "https://routing.openstreetmap.de/routed-foot/route/v1/foot"


# ---------- helpers ----------

def http_json(url, data=None, headers=None, timeout=TIMEOUT):
    hdrs = {"User-Agent": UA, "Accept": "application/json"}
    if headers:
        hdrs.update(headers)
    body = None
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        hdrs["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=hdrs)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def claude(system, user, max_tokens=400):
    """One small Claude call. Returns the text or None on any failure."""
    if not API_KEY:
        return None
    payload = {
        "model": MODEL,
        "max_tokens": max_tokens,
        "system": system,
        "messages": [{"role": "user", "content": user}],
        "output_config": {"effort": "low"},
    }
    try:
        res = http_json(
            "https://api.anthropic.com/v1/messages",
            data=payload,
            headers={"x-api-key": API_KEY, "anthropic-version": "2023-06-01"},
            timeout=8,
        )
    except Exception as e:  # network, 4xx/5xx, timeout
        log("claude error: %s" % e)
        return None
    if res.get("stop_reason") != "end_turn":
        log("claude stop_reason=%s" % res.get("stop_reason"))
        return None
    parts = [b.get("text", "") for b in res.get("content", []) if b.get("type") == "text"]
    return "".join(parts).strip() or None


def parse_json_blob(text):
    if not text:
        return None
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end < 0:
        return None
    try:
        return json.loads(text[start:end + 1])
    except Exception:
        return None


def log(msg):
    sys.stderr.write("[%s] %s\n" % (time.strftime("%H:%M:%S"), msg))


# ---------- external data ----------

DEST_SYSTEM = (
    "You turn an elderly Israeli's spoken Hebrew into a place search. "
    "Strip filler such as 'אני צריך להגיע ל', 'בבקשה', 'תביא אותי'. Expand common phrasings "
    "(e.g. 'קופת חולים בדיזנגוף' means a health clinic on Dizengoff street). If no city is "
    "mentioned, use the city given to you. Reply with JSON only: "
    '{"query": "<Hebrew query for Nominatim, street and city>", '
    '"display_name": "<short Hebrew name, max 6 words, to read aloud>"}'
)

WHERE_SYSTEM = (
    "You calm and orient an elderly person who feels lost on a bus journey in Israel. "
    "Answer in ONE Hebrew sentence of at most 14 simple words: where they are and what to do "
    "next. No questions, no apologies, no technical words, no English. Use the grammatical "
    "gender given to you."
)


def api_destination(body):
    text = (body.get("text") or "").strip()
    city = (body.get("city") or "תל אביב").strip()
    if not text:
        return {"ok": False}
    out = parse_json_blob(claude(DEST_SYSTEM, "City: %s\nSpeech: %s" % (city, text)))
    if not out or not out.get("query"):
        return {"ok": False}
    return {"ok": True, "query": out["query"], "display_name": out.get("display_name") or out["query"]}


MATCH_SYSTEM = (
    "You help an elderly person who feels lost on a bus journey in Israel. You get a list of "
    "named places near them and what they say they see. Decide which candidate they most likely "
    "see (spelling, spacing and hyphens may differ; they may be speaking from memory). Answer ONE "
    "calm Hebrew sentence of at most 14 simple words telling them where they are, next to that "
    "place. No questions, no apologies, no English. Use the grammatical gender given to you. "
    "Reply with JSON only: "
    '{"text": "<the sentence>", "match": "<the candidate name exactly as given, or null>"}'
)

_NIQQUD = re.compile("[\u0591-\u05c7]")
_PUNCT = re.compile(r"[\s\-\u05be\u2013\u2014\"'\u05f3\u05f4\u2019\u201c\u201d.,;:!?()/\\]+")


def norm_he(s):
    s = _NIQQUD.sub("", str(s or "")).lower()
    s = _PUNCT.sub("", s)
    if s.startswith("\u05d4") and len(s) > 2:  # leading ה
        s = s[1:]
    return s


def fuzzy_match(seen, candidates):
    n = norm_he(seen)
    if len(n) < 2:
        return None
    best = None
    for c in candidates:
        m = norm_he(c)
        if len(m) < 2:
            continue
        if n in m or m in n:
            if best is None or len(m) > len(norm_he(best)):
                best = c
    return best


def api_where_am_i(body):
    gender = "f" if body.get("gender") == "f" else "m"
    seen = (body.get("seen") or "").strip()
    cands = [str(c) for c in (body.get("candidates") or []) if str(c).strip()][:12]
    if seen:
        user = (
            "Gender: %s\nLocation: %s, %s\nNearest street: %s\nCurrent step: %s\nRoute: %s\n"
            "Candidates: %s\nThe person says they see: %s"
            % (gender, body.get("lat"), body.get("lon"), body.get("street", ""),
               body.get("step", ""), body.get("route", ""), json.dumps(cands, ensure_ascii=False), seen)
        )
        out = parse_json_blob(claude(MATCH_SYSTEM, user, max_tokens=160))
        if out and isinstance(out.get("text"), str) and out["text"].strip():
            m = out.get("match")
            return {"ok": True, "text": out["text"].strip().strip('"'), "match": m if m in cands else None}
        m = fuzzy_match(seen, cands)
        if not m:
            return {"ok": False}
        return {"ok": True, "text": ("את ליד %s." if gender == "f" else "אתה ליד %s.") % m, "match": m}
    user = (
        "Gender: %s\nLocation: %s, %s\nNearest street: %s\nCurrent step: %s\nRoute: %s"
        % (gender, body.get("lat"), body.get("lon"), body.get("street", ""),
           body.get("step", ""), body.get("route", ""))
    )
    text = claude(WHERE_SYSTEM, user, max_tokens=120)
    if not text:
        return {"ok": False}
    return {"ok": True, "text": text.strip().strip('"')}


# ---------- nearby places (Overpass) ----------

OVERPASS = "https://overpass-api.de/api/interpreter"
OVERPASS_MIRRORS = ["https://overpass.kumi.systems/api/interpreter", OVERPASS]
_nearby_cache = {}

AMENITY_HE = {
    "pharmacy": ("בית מרקחת", 0), "bank": ("בנק", 1),
    "clinic": ("מרפאה", 3), "doctors": ("מרפאה", 3), "hospital": ("מרפאה", 3),
    "post_office": ("דואר", 4), "school": ("בית ספר", 5), "place_of_worship": ("בית כנסת", 6),
}


def classify(tags):
    """-> (kind_he, priority) or None."""
    if tags.get("highway") == "bus_stop":
        return ("תחנת אוטובוס", 9)
    a = tags.get("amenity")
    if a in AMENITY_HE:
        return AMENITY_HE[a]
    if tags.get("shop") == "supermarket":
        return ("סופרמרקט", 2)
    if tags.get("leisure") == "park":
        return ("גן ציבורי", 7)
    if tags.get("shop"):
        return ("חנות", 8)
    if a == "cafe":
        return ("בית קפה", 8)
    if a in ("restaurant", "fast_food"):
        return ("מסעדה", 8)
    if a or tags.get("tourism"):
        return ("מקום", 8)
    return None


def api_nearby(lat, lon):
    key = (round(lat, 4), round(lon, 4))
    hit = _nearby_cache.get(key)
    if hit and time.time() - hit[0] < 600:
        return hit[1]
    around = "(around:120,%s,%s)" % (lat, lon)
    ql = (
        "[out:json][timeout:6];("
        'nwr%s["name"]["amenity"];nwr%s["name"]["shop"];nwr%s["name"]["tourism"];'
        'nwr%s["name"]["leisure"="park"];nwr%s["name"]["highway"="bus_stop"];'
        ");out center 80;" % ((around,) * 5)
    )
    res, last_err = None, None
    for endpoint in OVERPASS_MIRRORS:  # overpass-api.de is often "at capacity"
        try:
            req = urllib.request.Request(
                endpoint, data=urllib.parse.urlencode({"data": ql}).encode("utf-8"),
                headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=8) as resp:
                res = json.loads(resp.read().decode("utf-8"))
            break
        except Exception as e:
            last_err = e
    if res is None:
        raise last_err
    found, seen_names = [], set()
    for el in res.get("elements", []):
        tags = el.get("tags") or {}
        name = (tags.get("name:he") or tags.get("name") or "").strip()
        cls = classify(tags)
        c = el if "lat" in el else el.get("center") or {}
        if not name or not cls or "lat" not in c:
            continue
        dist = round(haversine(lat, lon, c["lat"], c["lon"]))
        if dist > 150 or name in seen_names:
            continue
        seen_names.add(name)
        found.append((cls[1], dist, {"name": name, "kind_he": cls[0], "dist": dist}))
    found.sort(key=lambda x: (x[0], x[1]))
    out = {"ok": True, "items": [f[2] for f in found[:8]]}
    _nearby_cache[key] = (time.time(), out)
    return out


def api_geocode(q, lat=None, lon=None):
    params = {"q": q, "format": "json", "countrycodes": "il", "accept-language": "he", "limit": 3}
    if lat and lon:
        d = 0.15
        params["viewbox"] = "%f,%f,%f,%f" % (float(lon) - d, float(lat) + d, float(lon) + d, float(lat) - d)
    res = http_json(NOMINATIM + "/search?" + urllib.parse.urlencode(params))
    if not res:
        # the service answered, the place simply does not exist → ask the user again
        return {"ok": True, "found": False}
    r = res[0]
    return {"ok": True, "found": True, "lat": float(r["lat"]), "lon": float(r["lon"]),
            "name": r.get("display_name", q)}


def api_reverse(lat, lon):
    params = {"lat": lat, "lon": lon, "format": "json", "accept-language": "he", "zoom": 17}
    res = http_json(NOMINATIM + "/reverse?" + urllib.parse.urlencode(params))
    a = res.get("address", {})
    return {"ok": True, "street": a.get("road", ""), "city": a.get("city") or a.get("town") or ""}


def api_walk(f, t):
    url = "%s/%s,%s;%s,%s?overview=full&geometries=geojson" % (OSRM, f[1], f[0], t[1], t[0])
    res = http_json(url)
    route = res["routes"][0]
    coords = [[c[1], c[0]] for c in route["geometry"]["coordinates"]]
    return {"ok": True, "meters": round(route["distance"]), "path": coords}


def stride(path, **params):
    return http_json(STRIDE + path + "?" + urllib.parse.urlencode(params), timeout=20)


def haversine(lat1, lon1, lat2, lon2):
    import math
    p = math.pi / 180
    a = (math.sin((lat2 - lat1) * p / 2) ** 2
         + math.cos(lat1 * p) * math.cos(lat2 * p) * math.sin((lon2 - lon1) * p / 2) ** 2)
    return 2 * 6371000 * math.asin(math.sqrt(a))


_city_cache = {}


def stops_in_city(city):
    """Stride has no lat/lon filter on stops, only city — fetch the city once an hour."""
    today = date.today().isoformat()
    hit = _city_cache.get(city)
    if hit and time.time() - hit[0] < 3600:
        return hit[1]
    # Nominatim writes "תל־אביב–יפו" (maqaf, en dash); Stride writes "תל אביב יפו"
    plain = re.sub(r"\s+", " ", re.sub(r"[\-\u05be\u2013\u2014]", " ", city)).strip()
    for variant in dict.fromkeys([plain, city, plain.replace(" ", "-")]):
        items = stride("/gtfs_stops/list", date_from=today, date_to=today, city=variant, limit=4000)
        if items:
            _city_cache[city] = (time.time(), items)
            return items
    return []


def stops_near(lat, lon, radius=500, limit=8):
    city = api_reverse(lat, lon).get("city") or ""
    if not city:
        return []
    near = []
    for s in stops_in_city(city):
        d = haversine(lat, lon, s["lat"], s["lon"])
        if d <= radius:
            near.append((d, {"id": s["id"], "name": s.get("name", ""), "lat": s["lat"], "lon": s["lon"]}))
    near.sort(key=lambda x: x[0])
    return [s for _, s in near[:limit]]


def iso_aware(dt):
    return dt.isoformat(timespec="seconds")


def api_plan(olat, olon, dlat, dlon):
    """Direct line only. Any gap in the data -> ok:false -> client fallback."""
    o_stops = stops_near(olat, olon)
    d_stops = stops_near(dlat, dlon)
    if not o_stops or not d_stops:
        return {"ok": False}
    now = datetime.now().astimezone()
    o_ids = ",".join(str(s["id"]) for s in o_stops)
    d_ids = ",".join(str(s["id"]) for s in d_stops)
    o_rs = stride("/gtfs_ride_stops/list", gtfs_stop_ids=o_ids, arrival_time_from=iso_aware(now),
                  arrival_time_to=iso_aware(now + timedelta(minutes=90)), limit=600)
    d_rs = stride("/gtfs_ride_stops/list", gtfs_stop_ids=d_ids, arrival_time_from=iso_aware(now),
                  arrival_time_to=iso_aware(now + timedelta(minutes=240)), limit=600)
    o_dist = {s["id"]: haversine(olat, olon, s["lat"], s["lon"]) for s in o_stops}
    d_dist = {s["id"]: haversine(dlat, dlon, s["lat"], s["lon"]) for s in d_stops}
    by_ride = {}
    for rs in d_rs:
        by_ride.setdefault(rs["gtfs_ride_id"], []).append(rs)
    best = None
    for rs in o_rs:
        for drs in by_ride.get(rs["gtfs_ride_id"], []):
            if drs["stop_sequence"] <= rs["stop_sequence"]:
                continue
            walk = o_dist[rs["gtfs_stop_id"]] + d_dist[drs["gtfs_stop_id"]]
            # shortest walking first (rounded to 100 m), then the earliest bus
            key = (round(walk / 100), rs["arrival_time"])
            if best is None or key < best[0]:
                best = (key, rs, drs)
    if not best:
        return {"ok": False, "reason": "no-direct"}
    _, o_rs, d_rs = best
    between = stride("/gtfs_ride_stops/list", gtfs_ride_ids=o_rs["gtfs_ride_id"],
                     arrival_time_from=o_rs["arrival_time"], arrival_time_to=d_rs["arrival_time"], limit=200)
    between = sorted(between, key=lambda x: x["stop_sequence"])
    stops = [{"name": x.get("gtfs_stop__name", ""), "lat": x["gtfs_stop__lat"], "lon": x["gtfs_stop__lon"]}
             for x in between if o_rs["stop_sequence"] < x["stop_sequence"] <= d_rs["stop_sequence"]]
    if not stops:
        return {"ok": False}
    long_name = o_rs.get("gtfs_route__route_long_name") or ""
    headsign = long_name.split("<->")[-1]
    headsign = re.sub(r"-\d+#?$", "", headsign).split("-")[0].split("/")[0].strip() or headsign.strip()
    dep = datetime.fromisoformat(o_rs["arrival_time"])
    minutes = max(1, int((dep - now).total_seconds() // 60))
    return {
        "ok": True,
        "line": str(o_rs.get("gtfs_route__route_short_name") or "?"),
        "headsign": headsign,
        "origin_stop": {"name": o_rs.get("gtfs_stop__name", ""), "lat": o_rs["gtfs_stop__lat"], "lon": o_rs["gtfs_stop__lon"]},
        "dest_stop": stops[-1],
        "stops": stops,
        "departs_in_min": minutes,
    }


# ---------- HTTP ----------

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def log_message(self, fmt, *args):
        log(fmt % args)

    def _json(self, obj, status=200):
        data = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _safe(self, fn):
        try:
            return fn()
        except Exception as e:
            log("upstream failed: %s" % e)
            return {"ok": False}

    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        q = {k: v[0] for k, v in urllib.parse.parse_qs(url.query).items()}
        if url.path == "/api/geocode":
            return self._json(self._safe(lambda: api_geocode(q.get("q", ""), q.get("lat"), q.get("lon"))))
        if url.path == "/api/reverse":
            return self._json(self._safe(lambda: api_reverse(q["lat"], q["lon"])))
        if url.path == "/api/walk":
            f = [float(x) for x in q["from"].split(",")]
            t = [float(x) for x in q["to"].split(",")]
            return self._json(self._safe(lambda: api_walk(f, t)))
        if url.path == "/api/plan":
            return self._json(self._safe(lambda: api_plan(float(q["olat"]), float(q["olon"]),
                                                         float(q["dlat"]), float(q["dlon"]))))
        if url.path == "/api/nearby":
            return self._json(self._safe(lambda: api_nearby(float(q["lat"]), float(q["lon"]))))
        if url.path == "/api/health":
            return self._json({"ok": True, "claude": bool(API_KEY)})
        if url.path == "/":
            self.path = "/index.html"
        return super().do_GET()

    def do_POST(self):
        length = int(self.headers.get("Content-Length") or 0)
        try:
            body = json.loads(self.rfile.read(length).decode("utf-8") or "{}")
        except Exception:
            body = {}
        if self.path == "/api/destination":
            return self._json(self._safe(lambda: api_destination(body)))
        if self.path == "/api/where-am-i":
            return self._json(self._safe(lambda: api_where_am_i(body)))
        return self._json({"ok": False}, 404)

    def end_headers(self):
        if self.path.endswith((".html", ".js", ".json", ".webmanifest")):
            self.send_header("Cache-Control", "no-cache")
        super().end_headers()


if __name__ == "__main__":
    if not API_KEY:
        log("ANTHROPIC_API_KEY is not set — Claude routes will answer ok:false and the app will use fallbacks.")
    log("לאן? serving %s on http://0.0.0.0:%d  (demo: http://localhost:%d/?demo=1)" % (ROOT, PORT, PORT))
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
