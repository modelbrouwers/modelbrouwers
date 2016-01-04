import 'jquery';


$(function() {

	$('fieldset').on('change, keyup', '.formset-form input[type="url"]', previewUrl);

});


let previewUrl = function(event) {
    let url = $(this).val();
    let $form = $(this).closest('.formset-form');
    let $img = $form.find('img');
    let $preview = $form.find('.preview');
    $preview.addClass('hidden'); // always hide, only show when real urls work

    let img = new Image();
    img.onload = function() {
        $form.find('img').attr('src', url);
        $preview.removeClass('hidden');
    };
    img.src = url; // trigger loading
};
