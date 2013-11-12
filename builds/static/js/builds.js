var img_extensions = ['jpg', 'jpeg', 'png'];
var own_albums = new Array();

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

	$('input.photo-url, input[type="checkbox"]').tooltip({
		track: true
	});

	// drag and drop photos
	$('#radio').buttonset();
	$('#add-albumphoto').click(show_photos_selector);
	$('#photos-list').on('change', '#id_album', function(){
		$('#photos-list').data('current-album', $(this).val());
		update_photos_selector();
	});

	/* links to photos */
	// hide last 9 blocks if they're empty
	$('li.photo-form:not(:first)').filter(function(index){
		return !$(this).find('.photo-url').val();
	}).hide();

	// update preview & do validation
	$('#photos-formset').on('keyup', 'input.photo-url', function(event){
		var img_src = $(this).val();
		var extension = img_src.split('.').pop();
		var preview = $(this).closest('fieldset').siblings('.preview');
		$(this).siblings('.error.jquery-validation').remove();

		if (img_extensions.indexOf(extension.toLowerCase()) > -1){
			var tpl = load_template('photo_preview');
			var context = {'img_src': img_src};
			var rendered_tpl = tpl(context);
			preview.html(rendered_tpl);
			update_photo_fields($(this), true);

			if($('.error.jquery-validation').length == 0){
				// allow submitting
				$(this).closest('form').unbind('submit');
				$('#submit-build').removeAttr('disabled');
			}
		} else {
			preview.html('');
			update_photo_fields($(this), false);

			if($(this).val()){
				// show invalid warning
				var tpl = load_template('invalid_img_url');
				$(tpl()).insertAfter($(this));

				// disable form
				$(this).closest('form').submit(function(event){
					event.preventDefault();
					return false;
				});
				// disable button
				$('#submit-build').prop('disabled', true);
			} else {
				if($('.error.jquery-validation').length == 0){
					// allow submitting
					$(this).closest('form').unbind('submit');
					$('#submit-build').removeAttr('disabled');
				}
			}
		}
	});
	// trigger event, just in case it's filled in and we're re-displaying the form
	$('#photos-formset input.photo-url:visible').keyup();
});

function update_photo_fields(url_input, show_next){
	var li_item = url_input.closest('li.photo-form');
	var next_li = li_item.next();

	if(url_input.val()){
		// something is filled in, so we add a line
		li_item.data('used', true);
		if(!next_li.is(':visible') && show_next){
			next_li.show();
		}
	} else {
		li_item.data('used', false);
		li_item.siblings('li.photo-form').filter(function(index){
			return (!$(this).data('used') && !show_next);
		}).hide();
	}
}

function show_photos_selector(){
	$('#builds-overview').hide();
	$('#div-loading').show();

	// ophalen albums via JSON call, via tastypie API!
	if(!own_albums.length){
		$.ajax(own_albums_url+'?limit=0', {
			async: false,
			success: function(json, textStatus, jqXHR){
				own_albums = json.objects;
			}
		});
	}

	var tpl = load_template('albums');
	var context = {
		'albums': own_albums,
		'photos': null
	};

	render_photos_tpl(context);

	$('#div-loading').hide();
	$('#id_album').change();
}

function update_photos_selector(){
	$('#div-loading, #photos-dropzone').show();
	// fetch the photos of the selected album
	var album_id = $('#photos-list').data('current-album');
	var photos = null;

	$.ajax(album_photos_url, {
		async: false,
		data: {'limit': 0, 'album': album_id},
		success: function(json, textStatus, jqXHR){
			photos = json.objects;
		}
	});

	var context = {
		'albums': own_albums,
		'photos': photos
	}

	render_photos_tpl(context);
	$('#div-loading').hide();
}

function render_photos_tpl(context){
	var tpl = load_template('albums');
	var rendered_tpl = $(tpl(context));
	// set the checked album
	var album_val = $('#photos-list').data('current-album');
	rendered_tpl.find('#id_album').val(album_val);
	$('#photos-list').html(rendered_tpl);
	fixVerticalCenter();
}
