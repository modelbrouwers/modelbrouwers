import { CrudConsumer, CrudConsumerObject } from "consumerjs";

import { API_ROOT } from "../constants";

class GroupBuildParticipant extends CrudConsumerObject {}

class GroupBuildParticipantConsumer extends CrudConsumer {
    constructor(
        endpoint = `${API_ROOT}api/v1/groupbuilds/participant`,
        objectClass = GroupBuildParticipant
    ) {
        super(endpoint, objectClass);
    }

    /**
     * Toggle the finished state of a groupbuild
     * @param  {Number} id ID of the groupbuild to toggle
     * @return {Promise}
     */
    setFinished(id, finished = true) {
        return this.patch(`/${id}/`, { finished });
    }
}

export { GroupBuildParticipantConsumer };
