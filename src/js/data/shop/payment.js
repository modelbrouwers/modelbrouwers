import { CrudConsumer, CrudConsumerObject } from "consumerjs";

import { API_ROOT } from "../../constants";

class Payment extends CrudConsumerObject {}

export class PaymentConsumer extends CrudConsumer {
    constructor(endpoint = `${API_ROOT}api/v1/shop`, objectClass = Payment) {
        super(endpoint, objectClass);
    }

    listMethods() {
        return this.get("/paymentmethod/");
    }

    listIdealBanks() {
        return this.get("/ideal_banks/");
    }
}
