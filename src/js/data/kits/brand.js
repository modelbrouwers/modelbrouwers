import {CrudConsumer, CrudConsumerObject} from 'consumerjs';

import {API_ROOT} from '../../constants';
import {handleValidationErrors} from '../utils';

class Brand extends CrudConsumerObject {}

class BrandConsumer extends CrudConsumer {
  constructor(endpoint = `${API_ROOT}api/v1/kits/brand/`, objectClass = Brand) {
    super(endpoint, objectClass);
  }

  list() {
    return this.get('');
  }

  filter(params) {
    return this.get('', params);
  }

  fromRaw(name) {
    return this.create({name}).catch(err => {
      return Promise.reject(handleValidationErrors(err));
    });
  }
}

export {Brand, BrandConsumer};
