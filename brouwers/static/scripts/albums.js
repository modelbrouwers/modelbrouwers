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
    
    $('.photo-container2 img.photo, .in-photo-navigation').mouseenter(function() {
        $('div.in-photo-navigation').css('visibility', 'visible');
    });
    $('.photo-container2 img.photo').mouseleave(function() {
        $('div.in-photo-navigation').css('visibility', 'hidden');
    });
    
    /* FIXME werkt nog niet al te goed...
    $('.album-column .album-title').mouseenter(function() {
        var title = $(this).find('a').attr('title');
        if (title.length > 19)
        {
            $(this).parent().css('overflow', 'visible');
            $(this).css('overflow', 'visible');
            $(this).css('width', '1000px');
            
            $(this).find('a').html(title);
            var width = $(this).find('a').css('width');
            $(this).css('width', width);
            $(this).css('background', 'white');
            $(this).parent().css('z-index', '10');
        }
    });
    $('.album-column .album-title').mouseleave(function() {
        $(this).parent().css('overflow', 'hidden');
        $(this).css('overflow', 'hidden');
        $(this).css('width', 'auto');
        $(this).parent().css('z-index', '1');
        $(this).css('background', 'auto');
        var title = $(this).find('a').attr('title');
        if (title.length > 19)
        {
            title=title.slice(0,16)+"...";
        }
        $(this).find('a').html(title);
    });
    */
    
    var searchfield = $("#id_search");
    if (searchfield.val() == ''){
        searchfield.val('albums doorzoeken...');
        searchfield.css('color', '#555');
    }
    
    searchfield.focus(function () {
        searchfield.val('');
        searchfield.css('color', 'auto');
        $(this).autocomplete({
            source: "/albums/search/",
            autoFocus: true,
            minLength: 3,
            delay: 0,
            select:  function(e, ui) {
                window.location = ui.item.url;
            }
        });
    });
    searchfield.blur(function () {
        if (searchfield.val() == ''){
            searchfield.css('color', '555');
            searchfield.val('albums doorzoeken...');
        }
    });
    // setting the album cover
    $('.album-photos-list a.photo img').mouseenter(function(){
        if (!$(this).parent().parent().hasClass('cover')){
            $(this).parent().find('img.set_cover').show();
        }
    });
    $('.album-photos-list a.photo img').mouseleave(function(){
        $(this).parent().find('img.set_cover').hide();
    });
    $('.album-photos-list a.photo img.set_cover').click(function(e){
        e.stopPropagation();
        var a = $(this).parent();
        var p_id = a.attr('id').slice(6);
        $.post('/albums/set_cover/', {'photo': p_id}, function(data){
            if (data == 1){//success
                $('.cover').removeClass('cover');
                a.parent().addClass("cover");
            }
        });
        return false; // don't follow the url
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
    
    
    

