/*
output date to top left
*/
function real_date() {
const today = new Date();
const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

let month = months[today.getMonth()];
let day = days[today.getDay()];
let dateNumber = today.getDate();
let year = today.getFullYear();

document.getElementById('dayOfWeek').innerHTML = day
document.getElementById('date').innerHTML = month + " " + dateNumber + "," + " " + year
}
real_date()
setInterval(real_date, 60000) // 1 minute


/*
output current time to top right
*/
function real_time() {
const now = new Date();
var hour = now.getHours()
if (hour == 12) {
  ampm = 'pm'
} else if (hour > 12) {
  hour = hour - 12
  ampm = 'pm'
} else {
  ampm = 'am'
}

// need a fix for midnight. we don't want to display the time as 00:00. we want 12:00
if (hour == 0) {
  hour = 12
}
var minute = now.getMinutes()
if (minute < 10) {
  minute = '0' + minute
}
var realtime = hour + ':' + minute + ampm

document.getElementById('time').innerHTML = realtime
}
real_time()
setInterval(real_time, 1000) // 1 second

async function weather() {
  const url = "/booth/weather";
        let response = await fetch(url, {method: "POST"});
        let responseJSON = await response.json();

        let temp = document.getElementById('weather');
        temp.innerHTML = `${responseJSON.temp}&deg;`;
} 
weather()
setInterval(weather, 900000) // 15 minutes

async function holiday() {
  const url = "/booth/holiday";
        let response = await fetch(url, {method: "POST"});
        let responseJSON = await response.json();
        
        // holiday element only present on closed.html
        try {
        let holidayElement = document.getElementById('holiday');
        holidayElement.innerHTML = responseJSON.holiday;
        }
        catch {'oh well'};
} 
holiday()

async function nowPlaying() {
  let titleElement = document.getElementById('nowPlaying');
  let notAvailable = "Program Name Not Available";
  try {
      const url = "/stream/status";
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

async function fetchBanner() {
  let bannerElement = document.getElementById("message");
  const url = "/booth/banner/content";
  let response = await fetch(url, { method: "POST" });
  let responseJSON = await response.json();
  bannerElement.innerHTML = responseJSON.banner
}

fetchBanner()
setInterval(fetchBanner, 30000) // 30 seconds