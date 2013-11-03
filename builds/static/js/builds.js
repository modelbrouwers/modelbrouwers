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
    // hide last 9 blocks
    $('li.photo-form:not(:first)').hide();

    $('#photos-formset').on('keyup', 'input.photo-url', function(){
    	update_photo_fields($(this));
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

function update_photo_fields(url_input){
	var li_item = url_input.closest('li.photo-form');
	var next_li = li_item.next();
	
	if(url_input.val()){
		// something is filled in, so we add a line
		li_item.data('used', true);
		if(!next_li.is(':visible')){
			// fix the order
			if(next_li.find('.order').val() == 1){
				var order = next_li.data('order');
				next_li.find('.order').val(order);
			}
			next_li.show();
		}
	} else {
		li_item.data('used', false);
		console.log(next_li.find('photo-url').val());
		console.log(next_li.find('.preview').html());
		var next_li_used = next_li.find('photo-url').val() || next_li.find('.preview').html() != '';
		if(next_li.is(':visible') && !next_li_used){
			next_li.hide();
		}
	}
}