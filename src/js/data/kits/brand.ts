import {CrudConsumer, CrudConsumerObject} from 'consumerjs';

import {get} from '@/data/api-client';

import {API_ROOT} from '../../constants';
import {handleValidationErrors} from '../utils';

export interface BrandData {
  id: number;
  name: string;
  is_active: boolean;
  // Ommitted for list endpoint
  logo: {
    small: string;
  };
}

export type ListBrandData = Omit<BrandData, 'logo'>;

export const listBrands = async (): Promise<ListBrandData[]> => {
  const responseData = await get<ListBrandData[]>('kits/brand/');
  return responseData!;
};

class Brand extends CrudConsumerObject {}

class BrandConsumer extends CrudConsumer {
  constructor(endpoint = `${API_ROOT}api/v1/kits/brand/`, objectClass = Brand) {
    super(endpoint, objectClass);
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
