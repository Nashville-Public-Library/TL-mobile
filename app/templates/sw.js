const CACHE_NAME = 'ntl-pwa-cache-{{version}}';

const FILES_TO_CACHE = [
    '/static/pages/index.html',
    '/static/pages/home.html',
    '/static/pages/about.html',
    '/static/pages/privacy.html',
    '/static/pages/feedback.html',
    '/static/pages/settings.html',
    '/static/pages/schedule.html',
    '/static/pages/podcasts.html',
    '/static/pages/podcast-loading.html',
    '/static/pages/daily/monday.html',
    '/static/pages/daily/tuesday.html',
    '/static/pages/daily/wednesday.html',
    '/static/pages/daily/thursday.html',
    '/static/pages/daily/friday.html',
    '/static/pages/daily/saturday.html',
    '/static/pages/daily/sunday.html',
    '/static/img/ntl-logo-512x512.png',
    '/static/img/ntl-logo-192x192.png',
    '/static/img/NTL-white-trim.png',
    '/static/img/NPL.svg',
    '/static/img/iaais.png',
    '/static/img/instagram.png',
    '/static/img/facebook.png',
    '/static/img/website.png',
    '/static/img/email.png',
    '/static/img/phone.png',
    '/static/img/scheduleLinePreview.png',
    '/static/img/broadcastSchedulePreview.png',
    '/static/img/programGuidePreview.png',
    '/static/img/back-button.png',
    '/static/img/location.png',
    '/static/img/about.png',
    '/static/img/rotate-phone.png',
    '/static/img/streamPauseGreen.png',
    '/static/img/streamPauseRed.png',
    '/static/img/streamPlayGreen.png',
    '/static/img/streamPlayRed.png',
    '/static/js/app.js'
];

const podcastImagesToCache = [
  "aarp",
  "able",
  "aroundworld",
  "atlantic",
  "bookpage",
  "checklist",
  "community",
  "consumer",
  "diabetes",
  "discover",
  "economist",
  "entertainment",
  "eyes",
  "fortune",
  "historical",
  "hourshortstories",
  "cirrus",
  "independent",
  "lgbt",
  "mens",
  "moneytalk",
  "ledger",
  "scene",
  "nationalgeo",
  "science",
  "nyt",
  "newyorker",
  "newsweek",
  "people",
  "pet",
  "pnstalks",
  "pns",
  "pnsyonder",
  "poetry",
  "prevention",
  "readersdigest",
  "rollingstone",
  "smithsonian",
  "sports",
  "tennessean",
  "opinion",
  "time",
  "town",
  "vanity",
  "wsj",
  "wired",
  "woman"
]

// Install — cache all static assets
self.addEventListener('install', (event) => {
  console.log('[ServiceWorker] Install');
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      cacheAllFiles(cache);
    })
  );
  self.skipWaiting();
});

function cacheAllFiles(cache){
  cacheStaticFiles(cache);
  cachePodcastImages(cache);
  return;
}

function cacheStaticFiles(cache) {
  console.log('[ServiceWorker] Caching app shell');
  return cache.addAll(FILES_TO_CACHE);
}

function generatePodcastImageURL(podcast) {
  return `https://assets.library.nashville.gov/talkinglibrary/shows/${podcast}/image.jpg`
}

async function cachePodcastImages(cache) {
  for (const image of podcastImagesToCache) {
    try {
      const url = generatePodcastImageURL(image);
      const request = new Request(url, {mode: "no-cors"});
      const response = await fetch(request);
      await cache.put(request, response);
    }
    catch (whoops) {
      console.log(whoops);
    }
  }
}

self.addEventListener('message', (event) => {
  if (event.data && event.data.action === 'skipWaiting') {
    self.skipWaiting();
  }
});


// Activate — clean up old caches
self.addEventListener('activate', (event) => {
  console.log('[ServiceWorker] Activate');
  event.waitUntil(
    caches.keys().then((keyList) =>
      Promise.all(
        keyList.map((key) => {
          if (key !== CACHE_NAME) {
            console.log('[ServiceWorker] Removing old cache:', key);
            return caches.delete(key);
          }
        })
      )
    ).then(() => {
      return self.clients.claim();
    })
  );
});


self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;

  const url = new URL(event.request.url);
  if (url.pathname.endsWith('.mp3')) return; // Don't cache or intercept audio. Too big and pointless.
  if (url.hostname.includes("weather.gov")) return;// don't cache the weather lol

  event.respondWith(
    caches.match(event.request, { ignoreSearch: true }).then(cached => {
      if (cached) {
        console.log('[SW] Serving from cache:', event.request.url);
        return cached;
      }
      console.log('[SW] Fetching from network:', event.request.url);
      return fetch(event.request).then(response => {
        return caches.open(CACHE_NAME).then(cache => {
          cache.put(event.request, response.clone());
          return response;
        });
      });
    }).catch(() => {
      console.log('[SW] Fetch failed; returning fallback for:', event.request.url);
      if (event.request.headers.get('accept').includes('text/html')) {
        return caches.match('/static/pages/home.html');
      }
    })
  );
});

