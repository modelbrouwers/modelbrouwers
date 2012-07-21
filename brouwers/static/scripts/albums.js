$(document).ready(function() {    
    $('.BBCode').focus(function(){
        $(this).select();
    });
    $('.BBCode').mouseup(function(e){
        e.preventDefault();
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
    
    
    

