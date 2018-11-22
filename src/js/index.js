import Router from "./router/router";
import KitreviewsPage from "./kitreviews/index";
import AlbumsPage from "./albums/index";
import BuildPage from "./builds/index";
import GroupBuildsPage from "./groupbuilds/index";

const pageMap = {
    kitreviews: KitreviewsPage,
    albums: AlbumsPage,
    builds: BuildPage,
    group_builds: GroupBuildsPage
};

// Start routing
new Router(pageMap).autoload();
