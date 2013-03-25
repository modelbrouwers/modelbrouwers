/* note about translations: all the translations of 'static' stuff happens
*  in the template where the variable is passed to the js.
*  This makes the configuration less complex & keeps the static nature of the .js
*/
// FIXME: initUI() -> clean up and make more general, current version produces nasty JS code
$(document).ready(function() {
    $('.no-javascript').remove(); //hide the warning
    fixVerticalCenter(); // vertical centering of images
    
    // BBCode stuff
    $('.BBCode').focus(function(){
        $(this).select();
    });
    $('.BBCode').mouseup(function(e){
        if(e.preventDefault) {
            e.preventDefault();
        }
        return false;
    });
    
    // show/hide edit, remove, restore icons
    $('#album_list').on('mouseover', 'a.album, a.album img', function(){
        $(this).closest('li.album').find('.edit, .remove, .restore').show();
    });
    $('#album_list').on('mouseout', 'a.album', function() {
        $(this).find('.edit, .remove, .restore').hide();
    });
    
    // init dialogs
    if ($('#new-album-dialog').length > 0){ // new album dialog
        $('#new-album-dialog').dialog({
			autoOpen: false,
			width: 800,
			modal: true,
			title: trans_new_album,
			buttons: [{
			    text: trans_save,
			    click: function(){
			        data = $('form#new-album').serializeArray();
			        $.post(
			            url_new,
			            data,
			            function (response){
			                $("#new-album-dialog").html(response.form);
							$('img').tooltip({
								track: true
							});
							if (response.status == '1'){ // no form errors
							    mode = response.album_write_mode;
							    if (mode == 'u'){
							        parent = $('ul#personal-albums');
							    } else {
							        parent = $('ul#public-albums');
							    }
							    parent.append(response.album_li);
							    $("#new-album-dialog").dialog('close');
							}
			            }
			        );
			    }}, {
			    text: trans_cancel,
			    click: function() {
			        $(this).dialog("close");
			    }
			}]
	    });
	}
    if ($('#edit-dialog').length > 0){ // edit album dialog
        $('#edit-dialog').dialog({
			autoOpen: false,
            /*height: 440,*/
            width: 800,
            modal: true,
            title: trans_edit_album,
            buttons: [{
                text: trans_save,
                click: function(){
		            data = $('#form-edit-album').serializeArray();
		            var album_id = $(this).find('input[name="album"]').val();
		            $.post(
		                url_edit,
		                data,
		                function (response){
		                    $("#edit-dialog").html(response);
		                    // this way, initUI sets the right interface
		                    $('#id_row_users, #id_albumgroup_set-TOTAL_FORMS, #id_albumgroup_set-INITIAL_FORMS, #id_albumgroup_set-MAX_NUM_FORMS').remove(); 
		                    initUI();
		                }
		            );
		        }}, {
		        text: trans_cancel,
		        click: function() {
		            $(this).dialog("close");
		            $(this).dialog("option", "height", 400);
		        }
		    }]
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
			title: trans_trash,
			buttons: [{
			    text: trans_confirm,
			    click: function(){
			        var album_id = $('#remove-album').val();
			        $.post(
			            url_remove,
			            {'album': album_id},
			            function (response){
			                if (response == 'ok'){
			                    $('li#album_'+album_id).remove();
			                    $('#remove-dialog').dialog("close");
			                } else {
			                    alert('Moving to trash failed.');
			                }
			            }
			        );
			    }}, {
			    text: trans_cancel,
			    click: function() {
			        $(this).dialog("close");
			    }
			}]
	    });
	}
    
    // opening of the appropriate dialogs
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
    
    // navigation arrows
    $('div.in-photo-navigation a').hide();
    $('#previous-photo, #next-photo').mouseenter(function() {
        $(this).find('a').show();
    });
    $('#previous-photo, #next-photo').mouseleave(function() {
        $(this).find('a').hide();
    });
    
    var searchfield = $("#id_search");
    if (searchfield.val() == ''){
        searchfield.val(trans_search_album);
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
            searchfield.val(trans_search_album);
        }
    });
    
    // setting the album cover & deleting
    $('.album-photos-list a.photo img').mouseenter(function(){
        if (!$(this).parent().parent().hasClass('cover')){
            $(this).parent().find('img.set_cover').show();
        }
        $(this).parent().find('img.delete').show();
    });
    $('.album-photos-list a.photo').mouseleave(function(){
        $(this).parent().parent().find('img.set_cover').hide();
        $(this).parent().parent().find('img.delete').hide();
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
    $('.album-photos-list a.photo img.delete').click(function(e){
        e.stopPropagation();
        var a = $(this).parent();
        var p_id = a.attr('id').slice(6);
        $.post('/albums/photo/delete/', {'photo': p_id}, function(data){
            if (data == 1){//success
                a.parent().remove();
            }
        });
        return false; // don't follow the url
    });
    try{
        initSortable($('#personal-albums'));
        initSortable($('#public-albums'));
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
    
    $('#id_writable_to').live('change', function(){
        var searchbox = $('input#search-users');
        if ($(this).val() == 'g'){ // writable for group
            searchbox.show();
            $('div#users').parent().parent().show();
            showLinkedUsers();
        } else {
            searchbox.hide();
            $('div#users').parent().parent().hide(); //hide the row
        }
    });
    $('#showCovers').live('click', function(){
        showCovers($(this));
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
function showCovers(element){
    if ($('ul#photo-navigation').hasClass('not-downloaded')){ // covers ophalen
        $("#photo-navigation").before('<img id=\"loading\" src=\"/static/images/loading_big.gif\" alt=\"Loading...\"/>');
        album_id = $('#id_album').val();
        $.get(
            url_covers,
	        {'album': album_id},
	        function (response){
	            $("#photo-navigation").html(response);
	            if (response != 0){
	                $('img#loading').remove();
	                $("#photo-navigation").removeClass('not-downloaded');
	            }
	        }
        );
    }
    if ($('#photo-navigation').css('display') == 'none')
    {
        $('#photo-navigation').show();
        //height = $('#photo-navigation').height();
        //new_height = height + $("#edit-dialog").dialog( "option", "height" )+20;
        //$('#edit-dialog').parent().css('top', '100px');
        //$("#edit-dialog").dialog( "option", "height", new_height );
        
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
        //new_height = $("#edit-dialog").dialog( "option", "height" ) - height - 20;
        //$("#edit-dialog").dialog( "option", "height", new_height );
    }
    return false;
}
function openEditDialog(event, element, album_id){
    if(event.preventDefault) {
        event.preventDefault();
    }
    $("#edit-dialog").html('<img src=\"/static/images/loading_big.gif\" alt=\"Loading...\" style=\"margin-top:5em;\"/>');
    if (typeof album_id == 'undefined'){
	    var li = $(element).closest('li.album');
	    var album_id = li.children('input[name="album_id"]').val();
	}
	
	$.get(
	    url_edit,
	    {'album': album_id},
	    function (response){
	        $("#edit-dialog").html(response);
	        initUI();
	    }
	);
	
	$("#edit-dialog").dialog("open");
	$('button').button();
	$(".ui-icon-closethick").click(function(){
	    $("#edit-dialog").dialog("option", "height", 600);
	});
    return false;
}

function initUI(){
    $('#id_hidden_cover').val($('#id_cover').val());
	var a = "<a href=\"#\" id=\"showCovers\">";
	a += "<u>" + trans_pick_cover + "</u></a>";
    $('#id_cover').replaceWith(a);
    // write permissions for groups
    initSearchBox();
}

function initSearchBox(){
    if ($('#id_albumgroup_set-0-users').length == 0){
        $.get(
            url_get_group,
            {'album': $('#id_album').val()},
	        function (response){
	            $('#id_row_cover').after(response);
	            $('.hide').hide();
	            $('#id_row_users').hide();
	            insertSearchbox();
	        }
        );
    } else {
        insertSearchbox();
    }
}

function insertSearchbox(){
    var writable_select = $('select#id_writable_to');
    var text_field = '<input type=\"text\" class=\"autocomplete\" id=\"search-users\" placeholder=\"'+ trans_find_users +'\"/>';
    var div_users = '<tr><td></td><td colspan=\"2\"><div id=\"users\"></div></td>';
    writable_select.after(text_field);
    writable_select.parent().parent().after(div_users);
    var searchbox = $('input#search-users');
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
    
    // trigger event
    $('select#id_writable_to').change();
    
    // search & autocomplete
    searchbox.focus(function(){
        searchbox.val('');
    });
    searchbox.blur(function(){
        searchbox.val('');
    });
    $('a.remove-user').live('click', function(event){
        var user_id = String($(this).data('user_id'));
        var multi_select = $('#id_albumgroup_set-0-users');
        var values = multi_select.val();
        var index = values.indexOf(user_id);
        var removed = values.splice(index, 1);
        multi_select.val(values);
        showLinkedUsers();
        return false;
    });
}

function showLinkedUsers(){
    var options = $('#id_albumgroup_set-0-users option:selected');
    var html = '';
    $.each(options, function(index, option){
        var opt = $(option);
        var name = opt.text();
        var user_id = opt.val();
        
        var element = '<a href=\"#\" class=\"remove-user\" title=\"' + trans_revoke_rights + '\" data-user_id=\"' + user_id + '\">';
        element += '<span class=\"user ui-state-hover ui-widget ui-corner-all ui-icon-closethick\">';
        element += name + '</span></a>';
        html += element;
    });
    $('div#users').html(html);
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
			    alert('Restoring failed.');
			}
		}
	);
    return false;
}
