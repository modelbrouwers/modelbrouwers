import Router from './router/router';
import KitreviewsPage from './kitreviews/index';

const pageMap = {kitreviews: KitreviewsPage};

// Start routing
new Router(pageMap).autoload();
