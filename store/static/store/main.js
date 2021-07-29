$(document).ready(() => {
    $('#input-main').submit((e) => {
        e.preventDefault()
        const req = $('#input-main').serialize()
        ajax(req)
    })

    $('#next_button').click((e) => {
        e.preventDefault()
        const req = $('#next_button').attr("href").slice(1)
        ajax(req)
    })

    $('#prev_button').click((e) => {
        e.preventDefault()
        const req = $('#prev_button').attr("href").slice(1)
        ajax(req)
    })

    function ajax(req) {
        $.ajax({
            url: $('#main-wrapper').attr("data-url"),
            data: req,
            success: (response) => {
                let products = $(response).filter('.product-wrapper').html()
                let paginator = $(response).find('#next_button').attr('href')
                let paginator2 = $(response).find('#prev_button').attr('href')
                console.log(paginator)
                // if (paginator === '?') {
                //     paginator = ''
                // }
                // if (paginator2 === '?') {
                //     paginator2 = ''
                // }
                $('.product-wrapper').html(products)
                $('#next_button').attr("href", paginator)
                $('#prev_button').attr("href", paginator2)
                history.replaceState(null, null, `?${req}`);
            }
        })
    }
})
