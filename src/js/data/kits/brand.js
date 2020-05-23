import { CrudConsumer, CrudConsumerObject } from "consumerjs";

import { handleValidationErrors } from "../utils";
import { API_ROOT } from "../../constants";

class Brand extends CrudConsumerObject {}

class BrandConsumer extends CrudConsumer {
    constructor(
        endpoint = `${API_ROOT}api/v1/kits/brand/`,
        objectClass = Brand
    ) {
        super(endpoint, objectClass);
    }

    list() {
        return this.get("");
    }

    fromRaw(name) {
        return this.create({ name }).catch(err => {
            return Promise.reject(handleValidationErrors(err));
        });
    }
}

export { Brand, BrandConsumer };
