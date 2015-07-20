var rotation = 0;

$(function() {
    $('td.help_text div').hide(); // hide the help texts

    $('img').tooltip({
        track: true
    });

    if ($.fn.datepicker) {
        $('input.date').datepicker();
    }
});

function showHelp(e){
    //close all (the others)
    if ($(e).css('display') == 'none') {
        $('span.help_text').hide();
    }
    $('td.help_text div').hide();
    $(e).parent().parent().find('td.help_text div').toggle();
    $(e).siblings('.help_text').toggle();
}

function add_message(msg){
    m = '<li class=\"{{ class }}\">{{ text }}</li>';
    m = m.replace("{{ class }}", msg.tag);
    m = m.replace("{{ text }}", msg.text);
    $('div#messages ul.messages').append(m);
    $('div#messages').show();
}

function fixVerticalCenter(){
    var anchor = $('a.album, a.photo');
    $.each(anchor, function(){
        var a_height = $(this).height();
        var img = $(this).children('img.thumb:first');
        var img_height = $(img).height();
        if (img_height > 0 && img_height != a_height){
            padding = (a_height - img_height) / 2;
            $(img).css('padding-top', padding);
            $(img).css('padding-bottom', padding);
        }
    });
}

// CSRF protection, code from Django docs
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
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
var csrf_token = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        }
    }
});

/* Implement a string formatter */
if (!String.prototype.format) {
    String.prototype.format = function() {
        var args = arguments;
        return this.replace(/{(\d+)}/g, function(match, number) {
            return typeof args[number] != 'undefined'? args[number] : match ;
        });
    };
}