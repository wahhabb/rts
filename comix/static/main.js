/**
 * Created by wahhab on 8/28/16.
 */
function add_to_cart(catalog_id, field) {
    // console.log("In addToCart");
    $.ajax({
        url: "/order/add/",
        type: "POST",
        data: {"catalog_id": catalog_id },

        success: function(json) {
            $('#cart-count').html(json['cart_count']);
            if (json['not_added']) {
                $('#already_in_cart').slideDown(400).delay(1400).hide(200);
            } else {
                $('#added_to_cart').html('Added to Cart').slideDown(400).delay(1400).hide(200);
            }
            // field.innerHTML = "In Cart";
            $(field).removeClass("btn-primary").addClass('non-btn').html('In Cart');
        },
        error: function(xhr, errmsg, err) {
            $('#results').html('Oops! We have encountered an error: ' + errmsg).show();
            console.log(xhr.status  + ": " + xhr.responseText);
        }
    });
    return 0;
}

function add_to_wish_list(issue_id) {
    $.ajax({
        url: "/order/to_wish_list/",
        type: "POST",
        data: {"issue_id": issue_id},

        success: function(json) {
            console.log(json);
            console.log("success--wish_list_add");
            if (json['not_added']) {
                alert('Please log in or sign up to save to Want List')
            } else {
                $('#added_to_cart').html('Added to Want List').slideDown(400).delay(1400).hide(200);
            }
        }
    });
}

function genreChosen($slug) {
    // Send to list for genre
    window.location = "/issues/?category=" + $slug;
}
function dosearch() {
    title_field = document.getElementById('search-box');
    title_search = title_field.value;
    title_field.className = 'form-input input-inline';
    if (title_search.length) {
        window.location = '/issues/?search=' + title_search
    } else {
    title_field.className = 'form-input input-inline error';
    }
}
$(function() {
    $(window).resize();
});

$(window).resize( function() {
    if ($(window).width() < 601) {
        if (!$('#search-bar h3').hasClass('btn3')) {
            $('#search_buttons').hide();
            $('#search-bar h3').addClass('btn3')
                .click(function () {
                    $('#search_buttons').toggle(400);
                });
        }
    } else {
        $('#search-bar h3').removeClass('btn3').unbind('click');
                $('#search_buttons').show(400);
    }
});


$(function() {
    $('#search-box').keydown(function (evnt) {
        var key = evnt.which;
        if (key == 13) {
            dosearch();
        }
    });

    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});
