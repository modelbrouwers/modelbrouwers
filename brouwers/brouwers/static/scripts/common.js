var rotation = 0;
$(document).ready(function(){
    $('td.help_text div').hide(); // hide the help texts
    
    $('img').tooltip({
    	track: true
    });
    
    now = new Date();
    d = now.getDate();
    m = now.getMonth() + 1;
    
    if (d == 1 && m == 4){
        n = Math.random();
        //console.log(n);
        if (n >= 0.40 && n <= 0.60){
            setTimeout(function(){setInterval(function(){rotate()}, 1)}, 30000);
        }
    }
});

function showHelp(e){
    //close all (the others)
    if ($(e).css('display') == 'none')
    {
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

function rotate(){
    if (rotation < 180){
        rotation += 1;
        rotateScreen(rotation);
    }
}

function rotateScreen(degrees){
    $('body').css('-webkit-transform', 'rotate('+degrees+'deg)');
    $('body').css('-moz-transform', 'rotate('+degrees+'deg)');
    $('body').css('-ms-transform', 'rotate('+degrees+'deg)');
    $('body').css('-o-transform', 'rotate('+degrees+'deg)');
    $('body').css('transform', 'rotate('+degrees+'deg)');
}

// CSRF protection, code from Django docs
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
