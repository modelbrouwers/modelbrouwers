/**
 * Router
 * Auto loads view based on app/view
 * Reads app/view from body tag data attribute
 */

export default class Router {
    /**
     * Autoloads the correct module based on app and view
     */
    autoload() {
        let module = this.getModule();

        console.log('autoload', module)
        if (!module) {
            return;
        }

        import(`../${module}`)
            .then(module => {
                new module.default({
                    objectId: this.getObjectId()
                });
            });
    }

    /**
     * Returns the module name based on app and view
     * @returns {string|undefined}
     */
    getModule() {
        let app = this.getApp(),
            view = this.getView();

        if (app && view) {
            return `${app}/${view}.js`;
        }
    }

    /**
     * Returns the current Django app name
     * @returns {string|undefined}
     */
    getApp() {
        let html = document.querySelector('html');
        return html.dataset.app;
    }

    /**
     * Returns the current Django view name
     * @returns {string|undefined}
     */
    getView() {
        let html = document.querySelector('html');
        return html.dataset.view;
    }

    /**
     * Returns the current Django object ID
     * @returns {int|undefined}
     */
    getObjectId() {
        let html = document.querySelector('html');
        let objectId = html.dataset.objectid;
        return objectId ? parseInt(objectId, 10) : undefined;
    }
}
