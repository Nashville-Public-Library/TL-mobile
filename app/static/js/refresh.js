// refresh page
function refresh_page() {
    window.location.reload();
}
function check_time() {
    // if the current minute matches one of the minutes below, refresh the page
    const current_time = new Date();
    let minute = current_time.getMinutes();
    const updateTimes = [0, 30];
    if (updateTimes.includes(minute)) {
        refresh_page();
    }
}
setInterval(check_time, 60000)