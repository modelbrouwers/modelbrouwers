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

    $('#add-albumphoto').click(show_photos_selector);
});


function show_photos_selector(){
	var tpl = load_template('albums');
	console.log(tpl);
}