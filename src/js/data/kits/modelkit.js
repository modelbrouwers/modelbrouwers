import { CrudConsumer, CrudConsumerObject } from "consumerjs";

import { handleValidationErrors } from "../utils";
import { API_ROOT } from "../../constants";

class ModelKit extends CrudConsumerObject {}

class ModelKitConsumer extends CrudConsumer {
    constructor(
        endpoint = `${API_ROOT}api/v1/kits/kit/`,
        objectClass = ModelKit
    ) {
        super(endpoint, objectClass);
    }

    list() {
        return this.get("");
    }

    filter(filters) {
        return this.get("", filters);
    }

    create(data) {
        return super.create(data).catch(err => {
            return Promise.reject(handleValidationErrors(err));
        });
    }
}

export { ModelKitConsumer };
