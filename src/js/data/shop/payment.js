import { CrudConsumer, CrudConsumerObject } from "consumerjs";

import { API_ROOT } from "../../constants";

class Payment extends CrudConsumerObject {}

export class PaymentConsumer extends CrudConsumer {
    constructor(endpoint = `${API_ROOT}api/v1/shop`, objectClass = Payment) {
        super(endpoint, objectClass);
    }

    listMethods() {
        return this.get("/paymentmethod");
    }

    // TODO Only lists iDeal banks for now, check if other listing endpoints necessary
    listMethodBanks(bank) {
        switch (bank) {
            case "iDEAL":
            default:
                return this.get("/ideal_banks");
        }
    }
}
