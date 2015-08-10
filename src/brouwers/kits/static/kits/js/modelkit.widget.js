import { ModelKit } from 'kits/js/models/ModelKit';

import 'jquery';
import 'scripts/jquery.serializeObject';


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


function refreshKits(event) {
    let $container = $(this).closest('[data-filters="true"');
    let filters = $container.serializeObject();

    // strip off the prefix
    for (let key in filters) {
        let newKey = key.replace('{0}-'.format(conf.prefix), '');
        filters[newKey] = filters[key];
        delete filters[key];
    }

    ModelKit.objects.filter(filters).done(kits => {
        console.log(kits);
    });
}
