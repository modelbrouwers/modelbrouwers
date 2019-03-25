import Router from "./router/router";
import KitreviewsPage from "./kitreviews/index";
import AlbumsPage from "./albums/index";
import BuildPage from "./builds/index";
import GroupBuildsPage from "./groupbuilds/index";
import ShopPage from "./shop/index";
import { locales } from "./translations/utils";
import { addLocaleData } from "react-intl";

addLocaleData(locales);

const pageMap = {
    kitreviews: KitreviewsPage,
    albums: AlbumsPage,
    builds: BuildPage,
    group_builds: GroupBuildsPage,
    shop: ShopPage
};

// Start routing
new Router(pageMap).autoload();
