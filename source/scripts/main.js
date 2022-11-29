onLoad()

function onLoad() {
    createProfilesAlt()
    createMusic()
    enableExtraBootstrapTooltips()
    replaceYearToCurrent()
}

function createProfilesAlt() {
    $.get("data/profiles.json", function (json) {
        json.reverse().forEach(data => {
            var contactRoot = document.createElement("a");
            contactRoot.href = data["url"]
            contactRoot.className = "profile-entry display-4 " + data["icon"] + " mr-2"
            var tooltip = data["name"]
            if (data.hasOwnProperty("tooltip")) tooltip += "<br><br>" + data["tooltip"]
            contactRoot.setAttribute("data-toggle", "tooltip")
            contactRoot.setAttribute("data-html", "true")
            contactRoot.title = tooltip
            $(contactRoot).tooltip() // Fuck this fucking JS
            $(".profiles").prepend(contactRoot)
        })
    }, "json")
}

function createMusic() {
    $.get("data/music.json", function (json) {
        json.reverse().forEach(data => {
            var musicRoot = document.createElement("a")
            musicRoot.className = "music-entry p-3" // remove "p-3" for square images
            musicRoot.href = data["url"]
            var img = document.createElement("img")
            img.src = "media/music/" + data["image"]
            img.alt = data["name"]
            img.className = "col music-entry-image p-0 rounded-circle border" // remove "rounded-circle border" for square images 
            var tooltip = data["name"]
            if (data.hasOwnProperty("tooltip")) tooltip += "<br><br>" + data["tooltip"]
            musicRoot.setAttribute("data-toggle", "tooltip")
            musicRoot.setAttribute("data-html", "true")
            musicRoot.title = tooltip
            $(musicRoot).tooltip() // Fuck this fucking JS
            musicRoot.appendChild(img)
            $(".music").prepend(musicRoot)
        })
    }, "json")
}

function enableExtraBootstrapTooltips() {
    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    })
}

function replaceYearToCurrent() {
    document.getElementById("year").innerHTML = new Date().getFullYear();
}
