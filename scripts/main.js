onLoad()

function onLoad() {
    createProfiles()
    createMusic()
    enableExtraBootstrapTooltips()
}

function createProfiles() {
    $.get("data/profiles.json", function (json) {
        json.reverse().forEach(data => {
            var contactRoot = document.createElement("div")
            contactRoot.className = "col profile-entry"
            var label = document.createElement("h5")
            label.className = "profile-entry-label d-inline-flex pt-2 pl-3"
            var icon = document.createElement("i")
            icon.className = data["icon"] + " mr-2"
            label.appendChild(icon)
            label.innerHTML += data["name"]
            if (data.hasOwnProperty("tooltip")) {
                label.setAttribute("data-toggle", "tooltip")
                label.setAttribute("data-html", "true")
                label.title = data["tooltip"]
                $(label).tooltip() // Fuck this fucking JS
            }
            if (data.hasOwnProperty("url")) {
                var link = document.createElement("a")
                link.href = data["url"]
                link.appendChild(label)
                contactRoot.appendChild(link)
            } else contactRoot.appendChild(label)
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
