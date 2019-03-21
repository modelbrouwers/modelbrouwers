import { CrudConsumer, CrudConsumerObject } from "consumerjs";
import Handlebars from "handlebars/dist/handlebars.min.js";

import { API_ROOT } from "../constants";

const TEMPLATE_CACHE = {};

class Template extends CrudConsumerObject {}

class TemplateConsumer extends CrudConsumer {
    constructor(endpoint = `${API_ROOT}templates/`, objectClass = Template) {
        super(endpoint, objectClass);

        this.defaultHeaders["Accept"] = "application/json";
    }

    loadTemplate(app, name) {
        const tplName = `${app}::${name}`;

        if (TEMPLATE_CACHE[tplName] != null) {
            const tpl = TEMPLATE_CACHE[tplName];
            return Promise.resolve(tpl);
        }

        return this.get(`${app}/${name}/`).then(response => {
            TEMPLATE_CACHE[tplName] = Handlebars.compile(response.template);
            return TEMPLATE_CACHE[tplName];
        });
    }
}

export default TemplateConsumer;
