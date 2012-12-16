$(document).ready(function(){
    $('td.help_text div').hide(); // hide the help texts
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
