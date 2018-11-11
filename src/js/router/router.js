/**
 * Router
 * Auto loads view based on page name, which is read from html tag data attribute
 */

export default class Router {
    constructor(pageMap) {
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
