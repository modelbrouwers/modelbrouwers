import Router from "./router/router";
import KitreviewsPage from "./kitreviews/index";
import AlbumsPage from "./albums/index";

const pageMap = { kitreviews: KitreviewsPage, albums: AlbumsPage };

// Start routing
new Router(pageMap).autoload();
