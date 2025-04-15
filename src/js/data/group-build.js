import {CrudConsumer, CrudConsumerObject} from 'consumerjs';

import {API_ROOT} from '../constants';

class GroupBuild extends CrudConsumerObject {}

class GroupBuildConsumer extends CrudConsumer {
  constructor(endpoint = `${API_ROOT}api/v1/groupbuilds/groupbuild`, objectClass = GroupBuild) {
    super(endpoint, objectClass);
  }
}

export {GroupBuildConsumer};
