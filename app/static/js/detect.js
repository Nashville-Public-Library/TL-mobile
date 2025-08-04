function sw() {
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js').then(reg => {
    console.log('[SW] Registered with scope:', reg.scope);

    // Always check for an update when the page becomes visible
    document.addEventListener('visibilitychange', () => {
      if (document.visibilityState === 'visible') {
        reg.update(); // 🔄 Triggers update check on visibility
      }
    });

    // Prompt the user when there's a waiting SW
    function promptUserToUpdate(sw) {
      const wantsUpdate = alert("Your app will now be updated to the newest version.");
        sw.addEventListener('statechange', () => {
          if (sw.state === 'activated') {
            window.location.reload(); // ✅ Reload only after new SW takes control
          }
        });
        sw.postMessage({ action: 'skipWaiting' }); // 🪄 Activates new SW
      
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

    // 🔥 Don't reload blindly on controllerchange — user decides!
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
  const warning = document.getElementById("orientationChange");
  if (isLandscape()) {
    warning.style.display = "block"
  } else {
    warning.style.display = "none"
  }
}

async function detect() {
    if (!isMobileDevice()) {
        document.body.innerHTML = "<div style='text-align: center; margin-top: 20%; font-size: 50pt; color: aliceblue;'>ONLY AVAILABLE ON MOBILE</div>";
        return;
    }

    const installed = window.matchMedia("(display-mode: standalone)").matches || window.navigator.standalone === true;
    // const installed = true;
    if (!installed) {
        console.log('not installed, fetching page');
        let response = await fetch('/static/pwa/pages/install.html');
        let text = await response.text()

        document.body.innerHTML = text;
        return;
    } else {
        sw()
        handleOrientationChange()
        
        window.addEventListener('resize', () =>{
          let orientationTimeout;
          clearTimeout(orientationTimeout);
          orientationTimeout = setTimeout(handleOrientationChange, 300);
        } )
        }
    }


detect()