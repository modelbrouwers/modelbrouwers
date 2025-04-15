import {CrudConsumer, CrudConsumerObject, LinkedPageNumberList} from 'consumerjs';

import {API_ROOT} from '../../constants';
import {handleValidationErrors} from '../utils';

class ModelKit extends CrudConsumerObject {}

class ModelKitConsumer extends CrudConsumer {
  constructor(endpoint = `${API_ROOT}api/v1/kits/kit/`, objectClass = ModelKit) {
    super(endpoint, objectClass, {
      parserDataPath: 'results',
      listClass: LinkedPageNumberList,
    });
  }

  list() {
    return this.get('');
  }

  filter(filters) {
    return this.get('', filters);
  }

  create(data) {
    return super.create(data).catch(err => {
      return Promise.reject(handleValidationErrors(err));
    });
  }
}

export {ModelKitConsumer};
