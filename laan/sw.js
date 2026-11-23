// לאן? service worker: shell offline, data always from the network.
const VERSION = "laan-v1";
const SHELL = "shell-" + VERSION;
const EXTERNAL = "ext-" + VERSION;
const EXTERNAL_MAX = 150;
const SHELL_FILES = ["/", "/index.html", "/manifest.json", "/icon.svg"];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(SHELL)
      // add one by one so a single missing file never blocks installation
      .then((c) => Promise.all(SHELL_FILES.map((u) => c.add(u).catch(() => {}))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(
        keys.filter((k) => k !== SHELL && k !== EXTERNAL).map((k) => caches.delete(k))
      ))
      .then(() => self.clients.claim())
  );
});

async function trim(cacheName, max) {
  const cache = await caches.open(cacheName);
  const keys = await cache.keys();
  for (let i = 0; i < keys.length - max; i++) await cache.delete(keys[i]); // oldest first
}

async function networkFirst(request) {
  const cache = await caches.open(SHELL);
  try {
    const res = await fetch(request);
    if (res && res.ok) cache.put(request, res.clone());
    return res;
  } catch (err) {
    const hit = await cache.match(request, { ignoreSearch: true });
    if (hit) return hit;
    if (request.mode === "navigate") {
      const page = (await cache.match("/index.html")) || (await cache.match("/"));
      if (page) return page;
    }
    throw err;
  }
}

async function staleWhileRevalidate(request) {
  const cache = await caches.open(EXTERNAL);
  const hit = await cache.match(request);
  const refresh = fetch(request)
    .then((res) => {
      // opaque responses (status 0) are fine to cache for tiles, scripts and fonts
      if (res && (res.ok || res.type === "opaque")) {
        cache.put(request, res.clone()).then(() => trim(EXTERNAL, EXTERNAL_MAX));
      }
      return res;
    })
    .catch(() => null);
  if (hit) {
    refresh.catch(() => {});
    return hit;
  }
  const res = await refresh;
  return res || Response.error();
}

self.addEventListener("fetch", (event) => {
  const request = event.request;
  if (request.method !== "GET") return;
  const url = new URL(request.url);

  if (url.origin === self.location.origin) {
    if (url.pathname.startsWith("/api/")) return; // always network, never cached
    event.respondWith(networkFirst(request));
    return;
  }
  if (url.protocol === "http:" || url.protocol === "https:") {
    event.respondWith(staleWhileRevalidate(request));
  }
});
