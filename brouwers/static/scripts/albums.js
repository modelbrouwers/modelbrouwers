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
    
    $('.photo-container2 img.photo').mouseenter(function() {
        $('div.in-photo-navigation').css('visibility', 'visible');
    });
    $('.photo-container2 img.photo').mouseleave(function() {
        $('div.in-photo-navigation').css('visibility', 'hidden');
    });
    
    $('.album-list .album-title').mouseenter(function() {
        var title = $(this).find('a').attr('title');
        if (title.length > 19)
        {
            $(this).parent().css('overflow', 'visible');
            $(this).css('overflow', 'visible');
            $(this).css('width', '600px');
            $(this).css('text-align', 'left');
            $(this).css('background', 'white');
            $(this).css('z-index', '10');
            $(this).find('a').html(title);
        }
    });
    $('.album-list .album-title').mouseleave(function() {
        $(this).parent().css('overflow', 'hidden');
        $(this).css('overflow', 'hidden');
        $(this).css('width', 'auto');
        $(this).css('text-align', 'center');
        $(this).css('z-index', '1');
        var title = $(this).find('a').attr('title');
        if (title.length > 19)
        {
            title=title.slice(0,16)+"...";
        }
        $(this).find('a').html(title);
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
    
    
    

