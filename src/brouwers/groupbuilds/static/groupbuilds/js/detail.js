'use strict';

import 'jquery';
import Api from 'scripts/api';


$(function() {
    $('[data-toggle="finished"]').click(function(e) {
        e.preventDefault();
        let endpoint = $(this).attr('href');
        let finished = $(this).children('.fa-times').length > 0;
        Api.request(endpoint, {finished: finished}).patch().done(response => {
            $(this).find('.fa').toggleClass('fa-times fa-check');
        });
        return false;
    })
});
