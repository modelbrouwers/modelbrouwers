import { CrudConsumer, CrudConsumerObject } from "consumerjs";

import { API_ROOT } from "../../constants";

class UserProfile extends CrudConsumerObject {}

export class UserProfileConsumer extends CrudConsumer {
    constructor(
        endpoint = `${API_ROOT}api/v1/user/profile`,
        objectClass = UserProfile
    ) {
        super(endpoint, objectClass);
    }

    fetch() {
        return this.get("/");
    }
}
