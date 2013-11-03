var img_extensions = ['jpg', 'jpeg', 'png'];

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

	/* links to photos */
	// hide last 9 blocks if they're empty
	$('li.photo-form:not(:first)').filter(function(index){
		return !$(this).find('.photo-url').val();
	}).hide();
	// hide order fields, they're set already
	$('.order').hide();

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
			update_photo_fields($(this));

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

function update_photo_fields(url_input, show_next){
	var li_item = url_input.closest('li.photo-form');
	var next_li = li_item.next();
	
	if(url_input.val()){
		// something is filled in, so we add a line
		li_item.data('used', true);
		if(!next_li.is(':visible') && show_next){
			// fix the order
			if(next_li.find('.order').val() == 1){
				var order = next_li.data('order');
				next_li.find('.order').val(order);
			}
			next_li.show();
		}
	} else {
		li_item.data('used', false);
		li_item.siblings('li.photo-form').filter(function(index){
			return !$(this).data('used');
		}).hide();
		// TODO: fix the order if removing urls midway
	}
}