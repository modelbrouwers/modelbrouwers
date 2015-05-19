$(function() {
    'use strict';

    $('.controls').on('click', '[data-action]', function(event) {
        event.preventDefault();
        var mutualExclusive,
            $control = $(this),
            $figure = $control.closest('figure');

        // remove active class from mutually exclusive controls
        $control.siblings().removeClass('active');

        // remove current action css class and add the correct class
        mutualExclusive = $.map($control.siblings(), function(el) {
            return $(el).data('action');
        });
        $figure
            .removeClass(mutualExclusive.join(' '))
            .addClass($control.data('action'));
        $control.addClass('active');
        return false;
    });
});
