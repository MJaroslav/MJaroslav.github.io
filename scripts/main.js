onLoad()

function onLoad() {
    createContacts()
    enableExtraBootstrapTooltips()
}

function createContacts() {
    $.get("data/contacts.json", function (json) {
        json.reverse().forEach(data => {
            var contactRoot = document.createElement("div")
            contactRoot.className = "col"
            var label = document.createElement("h5")
            label.className = "d-inline-flex pt-2 pl-3"
            var icon = document.createElement("i")
            icon.className = data["icon"] + " mr-2"
            label.appendChild(icon)
            label.innerHTML += data["name"]
            if (data.hasOwnProperty("tooltip")) {
                label.attributes += { "data-toggle": "toolptip", "data-html": "true" }
                label.title = data["tooltip"]
                $(label).tooltip()
            }
            if (data.hasOwnProperty("url")) {
                var link = document.createElement("a")
                link.href = data["url"]
                link.appendChild(label)
                contactRoot.appendChild(link)
            } else contactRoot.appendChild(label)
            $(".contacts").prepend(contactRoot)
        })
    }, "json")
}

function enableExtraBootstrapTooltips() {
    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    })
}
