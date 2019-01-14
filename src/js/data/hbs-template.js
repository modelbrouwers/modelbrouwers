import { CrudConsumer, CrudConsumerObject } from 'consumerjs';
import Handlebars from "handlebars/dist/handlebars.min.js";

import { API_ROOT } from '../constants';


const TEMPLATE_CACHE = {};


class Template extends CrudConsumerObject {}


class TemplateConsumer extends CrudConsumer {
    constructor(endpoint=`${API_ROOT}templates/`, objectClass=Template) {
        super(endpoint, objectClass);
    }

    loadTemplate(app, name) {
        const tplName = `${app}::${name}`;
        if (Handlebars.templates[tplName] != null) {
            const tpl = Handlebars.templates[tplName];
            return Promise.resolve(tpl);
        }

        return this
            .get(`${app}/${name}/`)
            .then(tpl => {
                Handlebars.templates[tplName] = Handlebars.compile(tpl);
                return Handlebars.templates[tplName];
            });
    }
}


export default TemplateConsumer;
