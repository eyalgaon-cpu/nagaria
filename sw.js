// Service Worker — נגרות אייל
// גרסה: כל שינוי כאן יגרום לעדכון אוטומטי
const CACHE_VERSION = 'nagaria-v3';
const CACHE_FILES = ['/nagaria/', '/nagaria/index.html', '/nagaria/manifest.json'];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE_VERSION).then(cache => cache.addAll(CACHE_FILES))
  );
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_VERSION).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', e => {
  // תמיד קודם מהרשת, cache כגיבוי
  e.respondWith(
    fetch(e.request).then(res => {
      const clone = res.clone();
      caches.open(CACHE_VERSION).then(cache => cache.put(e.request, clone));
      return res;
    }).catch(() => caches.match(e.request))
  );
});

// הודעה ל-client כשיש עדכון
self.addEventListener('message', e => {
  if (e.data === 'skipWaiting') self.skipWaiting();
});
