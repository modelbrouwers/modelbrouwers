var sidebar_html = "<div id=\"albums-sidebar\" class=\"opened\"></div>";
var restore_icon = '/static/images/icons/restore.png';
var close_icon = '/static/images/icons/remove2.png';
var prev_width = 0;

$(document).ready(function(){
    // sidebar loading etc.
    // TODO: add code to only do this for the beta testers
    if ($('textarea[name="message"]').length > 0){
        $('textarea[name="message"]').attr('id','id-textarea-post');
        $('#wrapfooter').after(sidebar_html);
        var sidebar = $("#albums-sidebar");
        
        $.get(
            '/albums/sidebar/',
            function(response){
                sidebar.html(response);
                sidebar.resizable({
                    ghost: true,
                    handles: "e",
                    maxWidth: 800
                });
                
                $('label').remove();
                selected_album = $('#id_album').val();
                window_height = $('body').height();
                console.log(selected_album);
                //TODO: get selected album & set title etc.
                
                /*$('#resizer').height(sidebar.height()-2);
                $('#resizer').resizable({
                    ghost: true,
                    handles: "e",
                    maxWidth: 800
                });*/
                
                $('#id_album').remove();
                $('#autocomplete-album').css('color', '#555');
                $('#autocomplete-album').focus(function () {
                    $(this).val('');
                    $(this).css('color', 'auto');
                    $(this).autocomplete({
                        source: "/albums/search_own_albums/",
                        autoFocus: true,
                        minLength: 2,
                        delay: 0,
                        select:  function(e, ui) {
                            loadPhotos(ui.item.album_id);
                        }
                    });
                });
                $('#autocomplete-album').blur(function () {
                    if ($(this).val() == ''){
                        $(this).css('color', '555');
                        $(this).val('Albums doorzoeken');
                    }
                });
            }
        );
        
        // options...
        $.get(
            '/albums/sidebar_color/',
            function (response){
                if (response != ''){
                    sidebar.css('background-color', response);
                }
            }
        );
        
        $('a.photo').live('click', function(e){
            e.preventDefault();
            var BBCode = $(this).attr('href')+"\n";
            insertAtCaret('id-textarea-post', BBCode);
            return false;
        });
        
        
        
        /* not required, position: fixed takes care of this
        var window_height = $('body').height();
        var sidebar_height = sidebar.height();
        var sidebar_top = parseInt(sidebar.css('top'), 10);
        var sidebar_total = sidebar_height + sidebar_top;
        
        // scrolling & moving of sidebar
        var lastScrollTop = 0;
        $(window).scroll(function(){
            var st = $(window).scrollTop();
            if (sidebar_total < window_height || st <= lastScrollTop){
            // also when scrolling up + prevent window height from increasing because of the scrolling
                sidebar.css("top", $(window).scrollTop() + "px");
            }
            window_height = $('body').height();
            sidebar_height = sidebar.height();
            sidebar_top = parseInt(sidebar.css('top'), 10);
            sidebar_total = sidebar_height + sidebar_top;
            lastScrollTop = st; 
        });
        */
    }
});
function loadPhotos(album_id){
    $.get(
        '/albums/get_photos/'+album_id+'/',
        function (response){
            $('#photos-list').replaceWith(response);
            //$("#albums-sidebar").tinyscrollbar();
            fixVerticalCenter();
        }
    );
}
function fixVerticalCenter(){
    var $a = $('a.album, a.photo');
    $.each($a, function(){
        var a_height = $(this).height();
        var img = $(this).children('img.thumb')[0];
        var img_height = $(img).attr('height');
        if (img_height > 0 && img_height != a_height){
            padding = (a_height - img_height) / 2;
            console.log(padding);
            $(img).css('padding-top', padding);
            $(img).css('padding-bottom', padding);
        }
    });
}
function toggleSidebar(){
    var sidebar = $('#albums-sidebar');
    if (sidebar.hasClass('opened')){
        sidebar.removeClass('opened');
        sidebar.addClass('closed');
        prev_width = parseInt(sidebar.width(), 10);
        sidebar.width('10');
        $('#control_icon').attr('src', restore_icon);
    } else {
        sidebar.removeClass('closed');
        sidebar.addClass('opened');
        sidebar.width('300');
        if (prev_width != 0){
            sidebar.width(prev_width);
        } else {
            sidebar.css('width', '30%');
        }
        $('#control_icon').attr('src', close_icon);
    }
}
function insertAtCaret(areaId,text) {
    var txtarea = document.getElementById(areaId);
    var scrollPos = txtarea.scrollTop;
    var strPos = 0;
    var br = ((txtarea.selectionStart || txtarea.selectionStart == '0') ? 
        "ff" : (document.selection ? "ie" : false ) );
    if (br == "ie") { 
        txtarea.focus();
        var range = document.selection.createRange();
        range.moveStart ('character', -txtarea.value.length);
        strPos = range.text.length;
    }
    else if (br == "ff") strPos = txtarea.selectionStart;

    var front = (txtarea.value).substring(0,strPos);  
    var back = (txtarea.value).substring(strPos,txtarea.value.length); 
    txtarea.value=front+text+back;
    strPos = strPos + text.length;
    if (br == "ie") { 
        txtarea.focus();
        var range = document.selection.createRange();
        range.moveStart ('character', -txtarea.value.length);
        range.moveStart ('character', strPos);
        range.moveEnd ('character', 0);
        range.select();
    }
    else if (br == "ff") {
        txtarea.selectionStart = strPos;
        txtarea.selectionEnd = strPos;
        txtarea.focus();
    }
    txtarea.scrollTop = scrollPos;
}
