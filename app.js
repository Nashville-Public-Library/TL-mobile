const routes = {
    '/': 'pages/home.html',
    '/schedule': 'pages/schedule.html',
    '/podcasts': 'pages/podcasts.html',
    '/broadcast-schedule': 'pages/broadcastSchedule.html',
    '/program-guide': 'pages/programGuide.html'
  };
  
  async function loadRoute() {
    const path = location.hash.slice(1) || '/';
    const route = routes[path];
  
    const app = document.getElementById('app');
    if (route) {
      const res = await fetch(route);
      const html = await res.text();
      app.innerHTML = html;
    } else {
      app.innerHTML = '<h1>Something went wrong. Not Found.</h1>';
    }
  }
  
  window.addEventListener('hashchange', loadRoute);
  window.addEventListener('DOMContentLoaded', loadRoute);
  

  async function nowPlaying() {
    let titleElement = document.getElementById('nowPlaying');
    let notAvailable = "Program Name Not Available";
    try {
        const url = "https://api.nashvilletalkinglibrary.com/stream/status";
        let response = await fetch(url, { method: "POST" });
        let icecast = await response.json();
        let nowPlaying = icecast.title;
        if (nowPlaying.trim() == "") {
            titleElement.innerText = notAvailable;
        }
        else {
            titleElement.innerText = nowPlaying;
  
        }
    }
    catch (whoops) {
        titleElement.innerText = notAvailable;
    }
  }
  nowPlaying()
  setInterval(nowPlaying, 60000) // 1 minute