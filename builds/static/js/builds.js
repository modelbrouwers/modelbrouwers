$(document).ready(function(){
	$('#id_search_term').autocomplete({
		source: search_url,
		autoFocus: true,
		minLength: 3,
		delay: 0,
		select:  function(e, ui) {
            window.location = ui.item.url;
        }
	});

	$('div.kit-info').hide();
	$('.handle').mouseenter(function(){
		$('div.kit-info').slideDown();
		$(this).addClass('opened');
	});
	$('.handle').click(function(){
		$(this).removeClass('opened');
		$('div.kit-info').slideUp();
	});

	$('input.order, input.photo-url').tooltip({
    	track: true
    });

	// drag and drop photos
	$('#radio').buttonset();
    $('#add-albumphoto').click(show_photos_selector);
    $('#photos-list').on('change', '#id_album', function(){
    	$('#photos-list').data('current-album', $(this).val());
    	update_photos_selector();
    });
});


function show_photos_selector(){
	$('#builds-overview').hide();
	$('#div-loading').show();

	var tpl = load_template('albums');
	var context = {
		'albums': new Array()
	};

	// ophalen albums via JSON call, via tastypie API!
	$.ajax(own_albums_url+'?limit=0', {
		async: false,
		success: function(json, textStatus, jqXHR){
			context.albums = json.objects;
		}
	});

	var rendered_tpl = $(tpl(context));
	// set the checked album
	rendered_tpl.find('#id_album').val($('#photos-list').data('current-album'));
	$('#photos-list').html($(rendered_tpl));
	$('#div-loading').hide();
}

function update_photos_selector(){
	console.log('I am updating');
}