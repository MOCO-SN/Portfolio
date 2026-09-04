const CACHE_NAME = 'profile-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/css/main.css',
  '/css/edu.css',
  '/css/projects.css',
  '/css/sidenav.css',
  '/css/cursor_tracking.css',
  '/css/links.css',
  '/css/progress.css',
  '/css/photos.css',
  '/css/supproted.css',
  '/css/loading.css',
  '/css/certificates.css',
  '/css/blog.css',
  '/js/main.js',
  '/js/project.js',
  '/js/sidenav.js',
  '/js/cursor_tracking.js',
  '/js/loading.js',
  '/js/blogs.js',
  '/js/photos.js',
  '/js/supported.js',
  '/js/changingtxt.js',
  '/favicon.png',
  '/res/cv.pdf'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        if (response) {
          return response;
        }
        return fetch(event.request).then(
          response => {
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }
            const responseToCache = response.clone();
            caches.open(CACHE_NAME)
              .then(cache => cache.put(event.request, responseToCache));
            return response;
          }
        );
      })
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});