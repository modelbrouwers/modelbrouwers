$(document).ready(function() {    
    $('.no-javascript').remove(); //hide the warning
    
    $('.BBCode').focus(function(){
        $(this).select();
    });
    $('.BBCode').mouseup(function(e){
        e.preventDefault();
    });
    
    //fix afbeeldingen verticaal centreren
    var $a = $('li.album a.album');
    $.each($a, function(){
        var a_height = $(this).height();
        var img = $(this).children('img.thumb')[0];
        var img_height = $(img).attr('height');
        if (img_height > 0 && img_height != a_height){
            padding = (a_height - img_height) / 2;
            $(img).css('padding-top', padding);
            $(img).css('padding-bottom', padding);
        }
    });
    
    $('a.album img').hover(function() {
        $(this).parent().find('.edit, .remove').show();
    });
    $('li.album').mouseout(function() {
        $(this).find('.edit, .remove').hide();
    });
    
    $('.photo-container2 img.photo, .in-photo-navigation').mouseenter(function() {
        $('div.in-photo-navigation').css('visibility', 'visible');
    });
    $('.photo-container2 img.photo').mouseleave(function() {
        $('div.in-photo-navigation').css('visibility', 'hidden');
    });
    
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
    try{
        initSortable($('#personal-albums'));
    }
    catch (err){
        //do nothing
    }
    $('#ShowAllAlbums').click(function(e){
        e.preventDefault();
        $.get(
            "/albums/all_own/",
            function (response){
                $('#personal-albums').replaceWith(response);
                initSortable($('#personal-albums'));
            }
        );
        return false;
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

function updateOrder(album, album_before, album_after){
    $.post(
        "/albums/reorder/",
        {
            'album': album, 
            'album_before': album_before,
            'album_after': album_after
        }
    );
}
function initSortable(element){
    element.sortable({
        placeholder: "sort-placeholder album",
        forcePlaceholderSize: true,
        helper: 'clone',
        forceHelperSize: true,
        opacity: 0.8,
        update: function(event, ui){
            var album = ui.item.find('input[name="album_id"]').val();
            var album_before = ui.item.prev().find('input[name="album_id"]').val();
            var album_after = ui.item.next().find('input[name="album_id"]').val();
            updateOrder(album, album_before, album_after);
        }
    });
}
