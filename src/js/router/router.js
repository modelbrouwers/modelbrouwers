/**
 * Router
 * Auto loads view based on page name, which is read from html tag data attribute
 */

/**
 * Load the relevant module dynamically.
 * @param  {String} name Alias of the page to load the module for.
 * @return {Promise}     Promise for the resolved default import.
 */
const loadModule = async (name) => {
    switch (name) {
        case "kitreviews":
            return import("../kitreviews/index");
        case "albums":
            return import("../albums/index");
        case "builds":
            return import("../builds/index");
        case "group_builds":
            return import("../groupbuilds/index");
        case "shop":
            return import("../shop/index");
        // some pages don't have an entrypoint at all, so don't throw exceptions
    }
};

export default class Router {
    static async route() {
        const page = this.getPage();
        try {
            const pageModule = await loadModule(page);
            pageModule.default.init();
        } catch (exc) {
            console.error(exc);
        }
    }

    /**
     * Returns the current page name
     * @returns {string|undefined}
     */
    static getPage() {
        let html = document.querySelector("html");
        return html.dataset.page;
    }
}
