const appVersion = "{{version}}";

function openlinkExternalWindow(url) {
  window.open(url, '_blank', 'noopener');
} 

function closeModalAlert() {
  const modalElement = document.getElementById("modalAlert");
  modalElement.style.display = "none";
  return;
}

function modalAlert(message) {
  const parent = document.getElementById("modalAlert");
  const content = document.getElementById("modalAlertMessage");
  content.innerText = message;
  parent.style.display = "block";

}

const routes = {
    '/': '/static/pages/home.html',
    '/about': '/static/pages/about.html',
    '/privacy': '/static/pages/privacy.html',
    '/schedule': '/static/pages/schedule.html',
    '/podcasts': '/static/pages/podcasts.html',
    '/podcasts-individual': '/static/pages/podcast-loading.html',
    '/schedule/monday': '/static/pages/daily/monday.html',
    '/schedule/tuesday': '/static/pages/daily/tuesday.html',
    '/schedule/wednesday': '/static/pages/daily/wednesday.html',
    '/schedule/thursday': '/static/pages/daily/thursday.html',
    '/schedule/friday': '/static/pages/daily/friday.html',
    '/schedule/saturday': '/static/pages/daily/saturday.html',
    '/schedule/sunday': '/static/pages/daily/sunday.html'
  };
  
  async function loadRoute() {
    const path = location.hash.slice(1) || '/';
    const route = routes[path];
  
    const app = document.getElementById('app');
    app.innerHTML = "<div> </div>"
    await new Promise(requestAnimationFrame);
    if (route) {
      const res = await fetch(route);
      const html = await res.text();
      app.innerHTML = html;
    } else {
      app.innerHTML = "<h1>We're so sorry, but something went wrong. Not Found.</h1>";
    }

    if (path === "/about") {
      loadAppVersion()
    }

    if (path === "/podcasts") {
      loadShowNamesInSearchInput()
      let categorySelected = sessionStorage.getItem("pocastCategory");
      if (categorySelected) {
        let categoryDropdown = document.getElementById("categorySelector");
        categoryDropdown.value = categorySelected
        categorySelector(categorySelected);
      }
    }
  }
  
  window.addEventListener('hashchange', loadRoute);
  window.addEventListener('DOMContentLoaded', loadRoute);

  function highlightNavBarIcon(icon) {
    icon.classList.add("icon-link-selected");
    const navLinks = document.getElementsByClassName("icon-link");
    for (var i = 0, len = navLinks.length; i < len; i++) {
      if (navLinks[i] != icon) {
        navLinks[i].classList.remove("icon-link-selected");
      }
    }
    document.getElementById("app").scrollTo({top: 0, behavior: "smooth"});
  }
  

  async function nowPlaying() {
    let titleElement = document.getElementById('nowPlaying');
    let livestream = document.getElementById("audio");
    let notAvailable = "Program Name Not Available";
    try {
        const url = "https://api.nashvilletalkinglibrary.com/stream/status";
        let response = await fetch(url, { method: "POST" });
        let icecast = await response.json();
        let nowPlaying = icecast.title;
        if (nowPlaying.trim() == "") {
            removeNowPlayingDots()
            titleElement.innerText = notAvailable;
            if (!livestream.paused) {updatePlayerMetadata(notAvailable);}
            return notAvailable;
        }
        else {
            removeNowPlayingDots()
            titleElement.innerText = nowPlaying;
            if (!livestream.paused) { updatePlayerMetadata(nowPlaying);}

            return nowPlaying;
        }
    }
    catch (whoops) {
        removeNowPlayingDots()
        titleElement.innerText = notAvailable;
        updatePlayerMetadata(notAvailable);
        return notAvailable;
    }
  }
  nowPlaying() // call on page load
  setInterval(nowPlaying, 30000) // 30 seconds

  function removeNowPlayingDots() {
      const nowPlayingDots = document.getElementById("nowPlayingDots");
      if (nowPlayingDots) {
        nowPlayingDots.remove()
      }

  }
  

  const button = document.getElementById('playPauseButton');
  button.addEventListener('click', () => {
  const audio = document.getElementById('audio');
    if (audio.paused) {
      if (!navigator.onLine){return;}
      nowPlaying()
      audio.src = "https://api.nashvilletalkinglibrary.com/stream/livestream.mp3"
      audio.play();
      switchPlayPauseIcon()
      button.setAttribute('aria-label', 'Pause');
    } else {
      audio.pause();
      switchPlayPauseIcon()
      button.setAttribute('aria-label', 'Play');
    }
  });

function switchPlayPauseIcon() {
  const playIcon = document.getElementById('playIcon');
  const pauseIcon = document.getElementById('pauseIcon');
  if (playIcon.style.display == "none") {
    pauseIcon.style.display = "none";
    playIcon.style.display = "block"
  } else {
    playIcon.style.display = "none";
    pauseIcon.style.display = "block"
  }
}



function updatePlayerMetadata(nowPlayingTitle) {
  const audio = document.getElementById('audio');
  if ('mediaSession' in navigator) {
    navigator.mediaSession.metadata = new MediaMetadata({
      title: nowPlayingTitle,
      artist: 'Nashville Talking Library',
      album: 'Live Stream',
      artwork: [
        { src: '/static/img/ntl-logo-192x192.png', sizes: '192x192', type: 'image/png' },
        { src: '/static/img/ntl-logo-512x512.png', sizes: '512x512', type: 'image/png' }
      ]
    });
    navigator.mediaSession.setActionHandler('play', () => {
      audio.play();
      switchPlayPauseIcon();
    });
    navigator.mediaSession.setActionHandler('pause', () => {
      audio.pause();
      switchPlayPauseIcon();
    });
    ['seekbackward', 'seekforward', 'previoustrack', 'nexttrack'] // we do not need these controls for the livestream.
      .forEach(a => { try { navigator.mediaSession.setActionHandler(a, null); } catch { } });
  }
}

function onlineOffline() {
  const onlineOfflineDotColor = document.getElementById("onlineOfflineDot");
  if (!navigator.onLine) {
    onlineOfflineDotColor.style.backgroundColor = "#f31642";
    modalAlert("You are not connected to the internet. The stream and other features will not work until you are back online.")
  } else {
    onlineOfflineDotColor.style.backgroundColor = "#00fc37";
  }
}
window.addEventListener('online', onlineOffline);
window.addEventListener('offline', onlineOffline);

// check on load
onlineOffline();

function loadAppVersion() {
  document.getElementById("appVersion").innerHTML = "v" + appVersion;
}

  async function loadPodcast(show) {  
    if (!navigator.onLine) {
      modalAlert("You cannot listen to podcasts while offline.")
      return;
    }
    location.hash = "/podcasts-individual"
    const app = document.getElementById("app"); // show the loading page, then go fetch the data from the server and render when ready

    const url = "/podcasts/info/" + show;
    let response = await fetch(url, { method: "POST", headers: {'Content-Type': 'text/html'}});
    if (response.ok) {
      let responseHTML = await response.text();
      app.innerHTML = responseHTML
      } else {
        app.innerHTML = "<h1>Sorry, we're having trouble fetching podcasts</h1>"
      }
    }

  function noPodcastWarning (show) {
    modalAlert(`We do not currently offer a podcast for ${show}.`);
  }


document.addEventListener('play', function (e) {
  var audios = document.getElementsByTagName('audio');
  for (var i = 0, len = audios.length; i < len; i++) {
    if (audios[i] != e.target) {
      audios[i].pause();
    }
  }

  if (e.target.id !== "audio") {
    const playIcon = document.getElementById('playIcon');
    const pauseIcon = document.getElementById('pauseIcon');
    playIcon.style.display = "block";
    pauseIcon.style.display = "none";
  }
}, true);

function categorySelector(category) {
  const podcasts = document.getElementsByClassName("podcastIndividual");
  const speed = 250;

  sessionStorage.setItem("pocastCategory", category)

  for (let i = 0; i < podcasts.length; i++) {
    let podcast = podcasts[i];

    // if set to 'all', show all podcasts
    if (category == "all") {
      podcast.style.display = "block";
      setTimeout(() => {
        podcast.style.opacity = '1';
      }, speed);
      continue; // next iteration
    }

    let categories = podcast.dataset.category.split(",");
    if (categories.includes(category)) {
      podcast.style.display = "block";
      setTimeout(() => {
        podcast.style.opacity = '1'
      }, speed);
    } else {
      podcast.style.opacity = "0";
      setTimeout(() => {
        podcast.style.display = "none";
      }, speed);

    }
  }
}

function podcastSearch(title) {
  const titleTrim = title.trim()
  if (titleTrim == "") {return;}

  const matchingElements = document.getElementsByClassName("podcastTitle");
  for (const match of matchingElements) {
    if (title == match.innerText) {
      let parentElementID = match.parentElement.id; // the ID of the parent element has the value of the directory on the server (the directory name of the show)
      loadPodcast(parentElementID);
      return;
    }
  }
  return;
}

function showMatchingTitleOnTextInput(text) {
  // first, reset the category selector so that any matching titles will be visible on the page.
  categorySelector("all");
  document.getElementById("categorySelector").value = "all";

  // once all titles are on the page, you can start filtering.
  const textLower = text.toLowerCase()
  const matchingElements = document.getElementsByClassName("podcastTitle");
  for (const match of matchingElements) {
    if (match.innerText.toLowerCase().includes(textLower)) {
      match.parentElement.style.display = "block"
    } else {
      match.parentElement.style.display = "none"
    }
  }
  return;
}

async function loadShowNamesInSearchInput() {
  const podcastTitles = document.getElementsByClassName("podcastTitle");
  const datalist = document.getElementById("podcastSearchList");

  for (const title of podcastTitles) {
    const option = document.createElement("option");
    option.value = title.innerText;
    datalist.appendChild(option)
  }
}

async function copyToClipboard(text) {
  await navigator.clipboard.writeText(text);
  modalAlert("RSS Feed copied to clipboard :)")
}