import 'bootstrap';
import 'bootstrap-datepicker';
import 'bootstrap-datepicker/js/locales/bootstrap-datepicker.nl';
import 'bootstrap-select';

import './csrf';

import Router from "./router/router";
import KitreviewsPage from "./kitreviews/index";
import AlbumsPage from "./albums/index";
import BuildPage from "./builds/index";
import GroupBuildsPage from "./groupbuilds/index";
// import ShopPage from "./shop/index";
// import { locales } from "./translations/utils";
// import { addLocaleData } from "react-intl";

// addLocaleData(locales);

const pageMap = {
    kitreviews: KitreviewsPage,
    albums: AlbumsPage,
    builds: BuildPage,
    group_builds: GroupBuildsPage,
    // shop: ShopPage
};

// Start routing
new Router(pageMap).autoload();

// global bootstrap stuff
$('.help').popover({
    'placement': 'auto right'
});

$('.badge').tooltip({
    'placement': 'auto left'
});

$('td.help_text div').hide(); // hide the help texts

$('img').tooltip({
    track: true
});

$('input.date').datepicker({
    language: 'nl',
    format: 'yyyy-mm-dd',
});
$('.selectpicker').selectpicker();
