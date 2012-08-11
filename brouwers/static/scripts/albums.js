$(document).ready(function() {    
    $('.no-javascript').remove(); //hide the warning
    
    $('.BBCode').focus(function(){
        $(this).select();
    });
    $('.BBCode').mouseup(function(e){
        e.preventDefault();
    });
    $('a.album img').hover(function() {
        $(this).parent().find('.edit, .remove').show();
    });
    $('div.album').mouseout(function() {
        $(this).find('.edit, .remove').hide();
    });
    
    
});

function hideNewAlbum(){
    $('div#new_album').html('');
    $('a#create_new_album').show();
}

function showHelp(e){
    //close all (the others)
    $('td.help_text div').hide();
    $(e).parent().parent().find('td.help_text div').show();
}
    
    
    

