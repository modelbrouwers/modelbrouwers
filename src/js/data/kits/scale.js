import { CrudConsumer, CrudConsumerObject } from "consumerjs";

import { handleValidationErrors } from "../utils";
import { API_ROOT } from "../../constants";

let reScale = new RegExp("1[/:]([0-9]*)");

const cleanScale = input => {
    if (isNaN(Number(input))) {
        let match = reScale.exec(input);
        if (match) {
            input = match[1];
        }
    }
    return input;
};

class Scale extends CrudConsumerObject {}

class ScaleConsumer extends CrudConsumer {
    constructor(
        endpoint = `${API_ROOT}api/v1/kits/scale/`,
        objectClass = Scale
    ) {
        super(endpoint, objectClass);
    }

    list() {
        return this.get("");
    }

    fromRaw(scale) {
        scale = cleanScale(scale);
        return this.create({ scale }).catch(err => {
            return Promise.reject(handleValidationErrors(err));
        });
    }
}

export { cleanScale, ScaleConsumer };
