onLoad()

function onLoad() {
    enableExtraBootstrapTooltips()
}

function enableExtraBootstrapTooltips() {
    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    })
}
