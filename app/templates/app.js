const appVersion = "{{version}}";

function openlinkExternalWindow(url) {
  window.open(url, '_blank', 'noopener');
} 

function openDefaultMailApp() {
  const toEmail = "ntl@nashville.gov";
  const subject = "NTL App Feedback";
  const userAgent = navigator.userAgent;
  const screenWidth = screen.width;
  const screenHeigt = screen.height;
  const screenSize = `${screenWidth}x${screenHeigt}`
  const version = appVersion;
  const doNotDelete = "The information above will help us to troubleshoot your issue. Please describe your issue in detail below this line:";
  const body = "Device: " + userAgent + "%0A" + "Version: " + version + "%0A" + "Screen: " + screenSize + "%0D%0A%0D%0A" + doNotDelete;
  window.open(`mailto:${toEmail}?subject=${subject}&body=${body}`, '_blank', 'noopener');
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
    '/feedback': '/static/pages/feedback.html',
    '/settings': '/static/pages/settings.html',
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
      const scroll = sessionStorage.getItem(path);
      if (scroll) { // if user has visited this page and we saved the last scroll position, scroll back to that position.
        app.scrollTo({top: scroll, behavior: "smooth"});
      }
    } else {
      app.innerHTML = "<h1>We're so sorry, but something went wrong. Not Found.</h1>";
    }

    if (path == "/") {
      fetchWeather();
    }

    if (path === "/about") {
      loadAppVersion()
    }

    if (path == "/settings") {
      fillSpeechSynthesisVoiceSelector();
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
  
  let currentRoute = location.hash.slice(1); // global variable to keep track of current page
  window.addEventListener('hashchange', () => {
    stopTextToSpeechGlobalAndHideButton(); // stop speaking whenever user loads new page
    saveScrollPositionAndLoadRoute(currentRoute);
  });
  
  window.addEventListener('DOMContentLoaded', loadRoute);

  function saveScrollPositionAndLoadRoute(routeToUpdate) {
    saveScrollPosition(routeToUpdate); // save scroll position on last visited page
    loadRoute(); // load the new page
    currentRoute = location.hash.slice(1); // update the global variable
  }

  function saveScrollPosition(routeToSaveScrollPosition) {
    let scrollPosition = document.getElementById("app").scrollTop;
    sessionStorage.setItem(routeToSaveScrollPosition, scrollPosition);
    return;
  }

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
      audio.src = "https://api.nashvilletalkinglibrary.com/stream/livestream.mp3";
      audio.play();
      switchPlayPauseIcon();
      button.setAttribute('aria-label', 'Pause');
    } else {
      audio.pause();
      audio.removeAttribute('src'); // or should we just set source to an empty string??  
      switchPlayPauseIcon();
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

function scheduleTextToSpeech() {
  document.getElementById("stopTextToSpeechGlobal").style.display = "inline-block";
  const todayElement = document.getElementsByClassName("dailyScheduleHeader");
  const todayInnerText = todayElement[0].innerText;
  const synth = window.speechSynthesis;
  const intro = getUserStoredVoiceSelection(`Here is the schedule for ${todayInnerText}`);
  synth.speak(intro);
  const allElements = document.getElementsByClassName("dailyScheduleContainerIndividual");
  let count = 0;
  for (let element of allElements) {
    let time = element.firstElementChild.innerText;
    let program = element.lastElementChild.innerText;
    const utterance = getUserStoredVoiceSelection(`${time}, ${program}`)
    synth.speak(utterance);
    utterance.onend = () => { // onend fires when the actual voice finishes speaking.
      count++;
      console.log(count, allElements.length)
      if(count == allElements.length) {
        // once we've looped through every element. This feels hacky...
        hideScheduleStopTextToSpeechButton();
  }
    }
  }
}

function stopTextToSpeechGlobalAndHideButton() {
  window.speechSynthesis.cancel();
  hideScheduleStopTextToSpeechButton()
}

function stopTextToSpeechGlobal() {
  window.speechSynthesis.cancel();
}

function hideScheduleStopTextToSpeechButton() {
  try {
  const stop = document.getElementById("stopTextToSpeechGlobal");
  stop.style.display = "none";
  }
  catch (error) {
    if (error instanceof TypeError) {
    // not to worry
    } else {
      console.log(error);
    }
  }
}

function fillSpeechSynthesisVoiceSelector() {
  const selectElement = document.getElementById("SpeechSynthesisVoiceSelector");
  const voices = window.speechSynthesis.getVoices()
  for (const voice of voices) {
    if (voice.lang.includes("en")) {
      const option = document.createElement("option");
      option.textContent = voice.name
      option.value = voice.name
      selectElement.appendChild(option)
    }
  }
  let previousSelection = localStorage.getItem("voice");
  selectElement.value = previousSelection;
}

function storeUserVoiceSelection(voice) {
  localStorage.setItem("voice", voice)
}

function getUserStoredVoiceSelection(toSpeak) {
  const speech = new SpeechSynthesisUtterance(toSpeak);

  let userSelectedVoice = localStorage.getItem("voice");
  if (userSelectedVoice) {
    const voices = window.speechSynthesis.getVoices();
    const voice = voices.find(v => v.name == userSelectedVoice);
    speech.voice = voice;
  }
  return speech;
}

function mobileOnlyTextToSpeech() {
  const elements = document.getElementsByClassName("mobileOnlySpeech");
  const synth = window.speechSynthesis;
  for (const element of elements) {
    const speech = new SpeechSynthesisUtterance(element.innerText)
    synth.speak(speech)
  }

}

async function fetchWeather() {
  const weatherElement = document.getElementById("weatherHomeScreen");
  const url = "https://api.weather.gov/gridpoints/OHX/50,57/forecast/hourly";
  const response = await fetch(url);
  const responseJSON = await response.json();

  const temp = responseJSON['properties']['periods'][0]['temperature'];
  const shortForecast = responseJSON['properties']['periods'][0]['shortForecast'];
  const chanceOfRain = responseJSON['properties']['periods'][0]['probabilityOfPrecipitation']['value'];
  weatherElement.innerHTML= `${temp}&deg; • ${shortForecast} • Chance of Rain: ${chanceOfRain}%`;
}