/**
 * Router
 * Auto loads view based on page name, which is read from html tag data attribute
 */

export default class Router {
    constructor(pageMap) {
        if (!pageMap) {
            throw new Error('A valid pageMap object is required for the router to function properly. Check the initialization of the router instance');
        }

        this.pageMap = pageMap;
    }

    /**
     * Autoloads the correct module based on page name
     */
    autoload() {
        let module = this.getPage();

        if (!module) {
            return;
        }

        this.pageMap[module].init();
    }

    /**
     * Returns the current page name
     * @returns {string|undefined}
     */
    getPage() {
        let html = document.querySelector('html');
        return html.dataset.page;
    }
}
