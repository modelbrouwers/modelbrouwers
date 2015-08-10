import { ModelKit } from 'kits/js/models/ModelKit';

import 'jquery';


let conf = {
    prefix: '__modelkitselect',
};


$(function() {

    console.log('loaded');

    let selBrand = '#id_{0}-brand'.format(conf.prefix);
    let selScale = '#id_{0}-scale'.format(conf.prefix);
    let $selects = $('{0}, {1}'.format(selBrand, selScale));

    $selects.change(refreshKits);


});


let refreshKits = function(event) {
    console.log(event);
};
