// Service Worker — נגרות אייל
// גרסה: כל שינוי כאן יגרום לעדכון אוטומטי
const CACHE_VERSION = 'nagaria-v4';

// index.html לא נשמר בקאש — תמיד נטען טרי מהרשת
const CACHE_FILES = ['/nagaria/manifest.json'];

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
  const url = new URL(e.request.url);

  // index.html — תמיד מהרשת, בלי קאש
  if (url.pathname === '/nagaria/' || url.pathname === '/nagaria/index.html') {
    e.respondWith(
      fetch(e.request, {cache: 'no-store'}).catch(() => caches.match(e.request))
    );
    return;
  }

  // שאר הקבצים — רשת קודם, קאש כגיבוי
  e.respondWith(
    fetch(e.request).then(res => {
      const clone = res.clone();
      caches.open(CACHE_VERSION).then(cache => cache.put(e.request, clone));
      return res;
    }).catch(() => caches.match(e.request))
  );
});

self.addEventListener('message', e => {
  if (e.data === 'skipWaiting') self.skipWaiting();
});
