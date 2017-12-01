if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
    var href = window.location.href
    if (!/\/m\//.test(href)) {
        window.location = href.replace('aollio.com', 'aollio.com/m')
    }
}
