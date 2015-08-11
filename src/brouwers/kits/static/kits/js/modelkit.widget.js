import { ModelKit } from 'kits/js/models/ModelKit';

import 'jquery';
import 'scripts/jquery.serializeObject';
import Handlebars from 'general/js/hbs-pony';


let conf = {
    prefix: '__modelkitselect',
    htmlname: 'kits',
    minChars: 2,
};


$(function() {

    console.log('loaded');

    let selBrand = '#id_{0}-brand'.format(conf.prefix);
    let selScale = '#id_{0}-scale'.format(conf.prefix);
    let selName = '#id_{0}-name'.format(conf.prefix);
    let $selects = $('{0}, {1}'.format(selBrand, selScale));

    $selects.change(refreshKits);
    $(selName).keyup(refreshKits);


});


function refreshKits(event) {
    let $container = $(this).closest('[data-filters="true"');
    let $target = $container.siblings('.kit-suggestions');
    let filters = $container.serializeObject();
    let checkedKits = [];

    if ($(this).is('input[type="text"]') && $(this).val() < conf.minChars) {
        return;
    }

    // strip off the prefix
    for (let key in filters) {
        let newKey = key.replace('{0}-'.format(conf.prefix), '');
        filters[newKey] = filters[key];
        delete filters[key];
    }

    ModelKit.objects.filter(filters).then(kits => {
        $target.find('.preview').filter((index, preview) => {
            let cb = $(preview).find('input[type="checkbox"]');
            let isChecked = cb.is(':checked');
            if (isChecked) {
                let id = $(preview).data('id');
                if (checkedKits.indexOf(id) === -1) {
                    checkedKits.push(id);
                }
            }
            return !isChecked;
        }).remove();

        // don't render the same kit again if it's in the list
        kits = kits.filter(kit => {
            return checkedKits.indexOf(kit.id) === -1;
        });

        return Handlebars.render('kits::select-modelkit-widget', {kits: kits, htmlname: conf.htmlname});
    }).done(html => {
        $target.append(html);
    });
}
