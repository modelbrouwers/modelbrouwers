import { CrudConsumer, CrudConsumerObject } from "consumerjs";

import { API_ROOT } from "../constants";

class Topic extends CrudConsumerObject {}

class TopicConsumer extends CrudConsumer {
    constructor(
        endpoint = `${API_ROOT}api/v1/forum_tools/topic/`,
        objectClass = Topic
    ) {
        super(endpoint, objectClass);
    }

    retrieve(id) {
        return this.read(`${id}/`);
    }
}

export { TopicConsumer };
