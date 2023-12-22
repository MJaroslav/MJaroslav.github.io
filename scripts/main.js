onLoad()

function onLoad() {
    enableExtraBootstrapTooltips()
    enableHeaderScrollDown()
}

function enableExtraBootstrapTooltips() {
    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    })
}

function enableHeaderScrollDown() {
    $('#header-scroll-down').click(function() {
        var target = $('header').outerHeight();
        $('html, body').animate({ scrollTop: target }, 400);
    })
}
