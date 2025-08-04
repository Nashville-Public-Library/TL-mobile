document.getElementById("selectMessage").addEventListener('change', fillBanner)
function fillBanner() {
    let selectMessage = document.getElementById("selectMessage");
    let box = document.getElementById("bannerMessage");
    box.value = selectMessage.value;
}

function validateBanner() {
    password = document.getElementById('password');
    if (password.value == '') {
        success = document.getElementById('success');
        success.style.display = 'block'
        // clear the emoji
        emoji = document.getElementById('emoji');
        emoji.remove()
    }
    else {
        form = document.getElementById('banner');
        form.submit();
    }
}

async function bannerContent() {
    const url = "/booth/banner/content"
    const options = { method: "POST" }
    let response = await fetch(url, options)
    let responseJSON = await response.json()

    const bannerMessageElement = document.getElementById("bannerMessage")

    bannerMessageElement.innerText = responseJSON.banner
}

window.onload = bannerContent()