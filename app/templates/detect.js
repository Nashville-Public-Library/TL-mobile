function sw() {
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js').then(reg => {
    console.log('[SW] Registered with scope:', reg.scope);

    // Always check for an update when the page becomes visible
    document.addEventListener('visibilitychange', () => {
      if (document.visibilityState === 'visible') {
        reg.update(); // Triggers update check on visibility
      }
    });

  async function reloadWindowAndModalAlert() {
    const parent = document.getElementById("modalAlertUpdateApp");
    const content = document.getElementById("modalAlertMessageUpdateApp");
    content.innerText = "Your app will now be updated to the newest version";
    parent.style.display = "block";
    const closeButton = document.getElementById("modalAlertButtonUpdateApp");
    closeButton.addEventListener("click", () => {
      window.location.reload();
});

}

    // Prompt the user when there's a waiting SW
    async function promptUserToUpdate(sw) {
        sw.addEventListener('statechange', () => {
          if (sw.state === 'activated') {
            reloadWindowAndModalAlert();
          }
        });
        sw.postMessage({ action: 'skipWaiting' }); // Activates new SW
      
    }

    // Handle case where a new SW is already waiting
    if (reg.waiting) {
      promptUserToUpdate(reg.waiting);
    }

    // Handle update found while app is running
    reg.addEventListener('updatefound', () => {
      const newSW = reg.installing;
      newSW.addEventListener('statechange', () => {
        if (newSW.state === 'installed' && navigator.serviceWorker.controller) {
          promptUserToUpdate(newSW); // only prompt if old SW is controlling
        }
      });
    });
  }).catch(err => {
    console.error('[SW] Registration failed:', err);
  });
}
}

function isMobileDevice () {
    const hover = window.matchMedia('(hover: none)').matches;
    const mobile = /mobi|Android|iPhone|iPad|iPod|Windows Phone/i.test(navigator.userAgent);
    if (hover || mobile) {return true;}
}

function isLandscape() {
  return window.innerWidth > window.innerHeight;
}

function handleOrientationChange() {
  return;
  const warning = document.getElementById("orientationChange");
  if (isLandscape()) {
    warning.style.display = "block"
  } else {
    warning.style.display = "none"
  }
}

function mobileOnlyTextToSpeech() {
  const elements = document.getElementsByClassName("mobileOnlySpeech");
  const synth = window.speechSynthesis;
  for (const element of elements) {
    const speech = new SpeechSynthesisUtterance(element.innerText)
    synth.speak(speech)
  }
}

function addMainScript() {
  const script = document.createElement("script");
  script.src = "/static/js/app.js";
  document.body.appendChild(script);
  return;
}

function makeBodyVisible() {
    document.body.classList.add("opacityOne");
}

async function detect() {
    if (!isMobileDevice()) {
      let response = await fetch('/static/pages/mobile-only.html');
      let text = await response.text();
        document.body.innerHTML = text;
        makeBodyVisible();
        return;
    }

    const installed = window.matchMedia("(display-mode: standalone)").matches || window.navigator.standalone === true;
    if (!installed) {
        console.log('not installed, fetching page');
        let response = await fetch('/static/pages/install.html');
        let text = await response.text()

        document.body.innerHTML = text;
        makeBodyVisible();
        return;
    } else {
        makeBodyVisible();
        addMainScript();
        sw();
        localStorage.setItem("appVersion", "{{version}}");
        handleOrientationChange();
        
        window.addEventListener('resize', () =>{
          let orientationTimeout;
          clearTimeout(orientationTimeout);
          orientationTimeout = setTimeout(handleOrientationChange, 300);
        } )
        }
    }


detect()