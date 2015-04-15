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
	$('#add-urlphoto').click(function(){
		$('input.photo-url').filter(function(){
			var preview = $(this).closest('fieldset').siblings('div.preview');
			return !preview.find('img').length;
		}).show();
		$('#photos-dropzone').hide();
	});
	$('#photos-list').on('change', '#id_album', function(){
		$('#photos-list').data('current-album', $(this).val());
		update_photos_selector();
	});

	/* links to photos */
	// hide last 9 blocks if they're empty
	$('li.photo-form:not(:first)').filter(function(index){
		var url_value = $(this).find('.photo-url').val();
		return !url_value;
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

	$('#photos-dropzone').droppable({
		accept: 'li.photo',
		activeClass: 'highlight',
		tolerance: 'intersect',
		drop: function(event, ui) {
			var photo = ui.draggable.data('id');
			var img_src = ui.draggable.find('div.full-image img').attr('src');

			var fieldset = $('fieldset:visible:last');
			var input_photo = fieldset.find('input.album-photo')
			input_photo.val(photo);

			var tpl = load_template('photo_preview');
			var context = {'img_src': img_src};
			var rendered_tpl = tpl(context);

			fieldset.siblings('div.preview').html(rendered_tpl);
			fieldset.closest('li').data('used', true);

			update_photo_fields(input_photo, true);
			ui.draggable.remove();
		}
	});

	// update previews in edit mode
	if (photo_urls){
		$('input.album-photo').each(function(i, e){
			var photo_id = $(this).val();
			var img_src = photo_urls[photo_id];
			if (img_src) {
				var preview = $(this).closest('fieldset').siblings('div.preview');

				var tpl = load_template('photo_preview');
				var context = {'img_src': img_src};
				var rendered_tpl = tpl(context);

				preview.html(rendered_tpl);
				$(this).closest('li.photo-form').show();
				$(this).siblings('input.photo-url, span.delete.checkbox').hide();

				update_photo_fields($(this), true);
			}
		});
	}

	// TODO: photo removed -> show url form
	// completely empty ->  check deleted checkbox
});

function update_photo_fields(input, show_next){
	var li_item = input.closest('li.photo-form');
	var next_li = li_item.next();

	if(input.val()){
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
	alert('Disabled because of issues - this will be fixed soon.');
	return;
	$('#builds-overview, input.photo-url, span.delete.checkbox').hide();
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

	// TODO: hide photos which have been selected already

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
	alert('Disabled because of issues - this will be fixed soon.');
	return;
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

	// initialize draggable
	$('#photos-list li.photo').draggable({
		containment: '#builds',
		// cursor: 'move',
		opacity: 0.7,
		revert: 'invalid',
		revertDuration: 200,
		helper: 'clone'
	});
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
