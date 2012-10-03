$(document).ready(function() {    
    $('.no-javascript').remove(); //hide the warning
    
    $('.BBCode').focus(function(){
        $(this).select();
    });
    $('.BBCode').mouseup(function(e){
        if(e.preventDefault) {
            e.preventDefault();
        }
        return false;
    });
    
    //fix afbeeldingen verticaal centreren
    fixVerticalCenter();
    
    $('a.album').hover(function() {
        $(this).find('.edit, .remove, .restore').show();
    });
    $('a.album img').hover(function() {
        $(this).parent().find('.edit, .remove, .restore').show();
    });
    $('li.album').mouseout(function() {
        $(this).find('.edit, .remove, .restore').hide();
    });
    
    if ($('#new-album-dialog').length > 0){
        $('#new-album-dialog').dialog({
			    autoOpen: false,
			    height: 400,
			    width: 800,
			    modal: true,
			    title: "Nieuw album",
			    buttons: {
			        "Bewaren": function(){
			            data = $('form#new-album').serializeArray();
			            $.post(
			                url_new,
			                data,
			                function (response){
			                    $("#new-album-dialog").html(response);
			                }
			            );
			        },
			        "Annuleren": function() {
			            $(this).dialog("close");
			        }
			    }
	    });
	}
    if ($('#edit-dialog').length > 0){
        $('#edit-dialog').dialog({
			    autoOpen: false,
			    height: 440,
			    width: 800,
			    modal: true,
			    title: "Album bewerken",
			    buttons: {
			        "Opslaan": function(){
			            data = $('#form-edit-album').serializeArray();
			            var album_id = $(this).find('input[name="album"]').val();
			            $.post(
			                url_edit,
			                data,
			                function (response){
			                        $("#edit-dialog").html(response);
			                }
			            );
			        },
			        "Annuleren": function() {
			            $(this).dialog("close");
			            $(this).dialog("option", "height", 400);
			        }
			    }
	    });
	}
	if ($('#remove-dialog').length > 0){
        $('#remove-dialog').dialog({
			autoOpen: false,
			draggable: false,
			dialogClass: "remove-album",
			height: 200,
			width: 400,
			modal: true,
			title: "Naar prullenbak?",
			buttons: {
			    Bevestig: function(){
			        var album_id = $('#remove-album').val();
			        $.post(
			            url_remove,
			            {'album': album_id},
			            function (response){
			                if (response == 'ok'){
			                    $('li#album_'+album_id).remove();
			                    $('#remove-dialog').dialog("close");
			                } else {
			                    alert('Het verwijderen is niet geslaagd.');
			                }
			            }
			        );
			    },
			    Annuleren: function() {
			        $(this).dialog("close");
			    }
			}
	    });
	}
    
    $('img.edit').click(function(e){
    	openEditDialog(e, $(this));
    });
    
    $('img.remove').click(function(e){
    	openRemoveDialog(e, $(this));
    });
    
    $('img.restore').click(function(e){
    	restoreAlbum(e, $(this));
    });
    $('a#new-album-popup').click(function(e){
        if(e.preventDefault) {
            e.preventDefault();
        }
        $('#new-album-dialog').dialog('open');
        return false;
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
        if(e.preventDefault) {
            e.preventDefault();
        }
        $.get(
            "/albums/all_own/",
            function (response){
                $('#personal-albums').replaceWith(response);
                initSortable($('#personal-albums'));
                fixVerticalCenter();
            }
        );
        return false;
    });
});

function hideNewAlbum(){
    $('div#new_album').html('');
    $('a#create_new_album').show();
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
function fixVerticalCenter(){
    var $a = $('a.album, a.photo');
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
function showCovers(){
    if ($('#photo-navigation').css('display') == 'none')
    {
        $('#photo-navigation').show();
        height = $('#photo-navigation').height();
        new_height = height + $("#edit-dialog").dialog( "option", "height" )+20;
        $('#edit-dialog').parent().css('top', '100px');
        $("#edit-dialog").dialog( "option", "height", new_height );
        
        $('#edit-dialog #photo-navigation img').click(function(){
            var p_id = $(this).next().val();
            $('#form-edit-album input[name="cover"]').val(p_id);
            $('#photo-navigation li').removeClass('cover');
            $(this).closest('li').addClass('cover');
        });
    }
    else
    {
        height = $('#photo-navigation').height();
        $('#photo-navigation').hide();
        new_height = $("#edit-dialog").dialog( "option", "height" ) - height - 20;
        $("#edit-dialog").dialog( "option", "height", new_height );
    }
    return false;
}
function openEditDialog(event, element, album_id){
    if(event.preventDefault) {
        event.preventDefault();
    }
    return false;
    if (typeof album_id == 'undefined'){
	    var li = $(element).closest('li.album');
	    var album_id = li.children('input[name="album_id"]').val();
	}
	$.get(
	    url_edit,
	    {'album': album_id},
	    function (response){
	        $("#edit-dialog").html(response);
	        
	        $('#id_hidden_cover').val($('#id_cover').val());
	        var a = "<a href=\"#\" onclick=\"showCovers();\">";
	        a += "<u>Cover kiezen</u></a>";
                $('#id_cover').replaceWith(a);
                // write permissions for groups
                initSearchBox();
	    }
	);
	
	$("#edit-dialog").dialog("open");
	$('button').button();
	$(".ui-icon-closethick").click(function(){
	    $("#edit-dialog").dialog("option", "height", 600);
	});
    return false;
}

function initSearchBox(){
    $('#id_albumgroup_set-0-users').parent().parent().hide();
    var writable_select = $('#id_writable_to');
    var text_field = '<input type=\"text\" class=\"autocomplete\" id=\"search-users\" placeholder=\"gebruikers zoeken...\"/>';
    var div_users = '<tr><td></td><td colspan=\"2\"><div id=\"users\"></div></td>';
    writable_select.after(text_field);
    writable_select.parent().parent().after(div_users);
    
    var searchbox = $('#search-users');
    writable_select.change(function(){
        if (writable_select.val() == 'g'){ // writable for group
            searchbox.show();
            $('div#users').parent().parent().show();
            showLinkedUsers();
        } else {
            searchbox.hide();
            $('div#users').parent().parent().hide(); //hide the row
        }
    });
    // trigger event
    writable_select.change();
    
    // search & autocomplete
    searchbox.focus(function(){
        searchbox.val('');
    });
    searchbox.blur(function(){
        searchbox.val('');
    });
    searchbox.autocomplete({
        source: user_search_url,
        autoFocus: true,
        minLength: 3,
        delay: 0,
        select:  function(e, ui) {
            var multi_select = $('#id_albumgroup_set-0-users');
            var user_id = String(ui.item.id);
            var values = multi_select.val();
            if (values == null){values=new Array();}
            values.push(user_id);
            multi_select.val(values);
            showLinkedUsers();
        }
    });
    $('a.remove-user').live('click', function(event){
        var user_id = String($(this).data('user_id'));
        var multi_select = $('#id_albumgroup_set-0-users');
        var values = multi_select.val();
        var index = values.indexOf(user_id);
        var removed = values.splice(index, 1);
        multi_select.val(values);
        showLinkedUsers();
    });
    
}
function showLinkedUsers()
{
    var options = $('#id_albumgroup_set-0-users option:selected');
    var html = '';
    $.each(options, function(index, option){
        var opt = $(option);
        var name = opt.text();
        var user_id = opt.val();
        
        var element = '<a href=\"#\" class=\"remove-user\" title=\"klik om rechten in te trekken\" data-user_id=\"' + user_id + '\">';
        element += '<span class=\"user ui-state-hover ui-widget ui-corner-all ui-icon-closethick\">';
        element += name + '</span></a>';
        html += element;
    });
    $('#users').html(html);
}


function openRemoveDialog(event, element){
    if(event.preventDefault) {
        event.preventDefault();
    }
    var li = $(element).closest('li.album');
    remove_album_id = li.children('input[name="album_id"]').val();
    $('#remove-album').val(remove_album_id);
    $.get(
        url_get_title,
        {'album': remove_album_id},
        function (title){
            $("span#id-album-title").text(title);
        }
    );
    $("#remove-dialog").dialog("open");
    return false;
}
function restoreAlbum(event, element){
    if(event.preventDefault) {
        event.preventDefault();
    }
    var li = $(element).closest('li.album');
    album_id = li.children('input[name="album_id"]').val();
    
    $.post(
        url_restore,
		{'album': album_id},
		function (response){
		    if (response == 'ok'){
			    $('li#album_'+album_id).remove();
			} else {
			    alert('Het terugzetten is niet geslaagd.');
			}
		}
	);
    return false;
}
