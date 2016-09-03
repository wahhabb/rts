/**
 * Created by wahhab on 8/28/16.
 */
function add_to_cart(catalog_id) {
    console.log("In addToCart");

    $.ajax({
        url: "/cart/add/",
        type: "POST",
        data: {"catalog_id": catalog_id },

        success: function(json) {
            console.log(json);
            console.log("success");
        },
        error: function(xhr, errmsg, err) {
            $('#results').html('Oops! We have encountered an error: ' + errmsg).show();
            console.log(xhr.status  + ": " + xhr.responseText);
        }
    });
    return 0;
}
var prev_order = "price-down";
function sortby(order) {
    if (order !== prev_order) {
        var qs = "{{ query_string|safe }}";
        if (qs.search(/(.+)&sort=.+(&*.*)/) > -1) {
            window.location = '?page=1' + qs.replace(/(.+)&sort=[^&]+(.*)/, '$1&sort=' + order);
            //    window.location = '?page=1' + qs.replace(/(.+)&sort=[^&]+(.*)/, '$1&sort=price-down');
        } else {
            window.location = '?page=1' + qs + '&sort=' + order;
        }

    }
}

$(function() {
    $('#title_search_btn').click(function () {
        $('#category_block').slideUp();
        $('#tag_block').slideUp();
        $('#search_block').slideDown("slow");
        return false;
    });
    $('#category_search_btn').click(function () {
        $('#category_block').slideDown("slow");
        $('#search_block').slideUp();
        $('#tag_block').slideUp();
        return false;
    });
    $('#tag_search_btn').click(function () {
        $('#category_block').slideUp();
        $('#search_block').slideUp();
        $('#tag_block').slideDown("slow");
        return false;
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
