import {CrudConsumer, CrudConsumerObject, LinkedPageNumberList} from 'consumerjs';

import {get, post} from '@/data/api-client';

import {API_ROOT} from '../../constants';
import {handleValidationErrors} from '../utils';

interface ListQueryParameters {
  /**
   * ID of the brand.
   */
  brand?: number;
  /**
   * ID of the scale.
   */
  scale?: number;
  /**
   * Partial (case insensitive) name search term.
   */
  name?: string;
  /**
   * Page number, 1-indexed.
   */
  page?: number;
}

interface BrandData {
  id: number;
  name: string;
  is_active: boolean;
  // Ommitted for list endpoint
  logo: {
    small: string;
  };
}

interface ScaleData {
  id: number;
  scale: number;
  __str__: string;
}

interface ModelKitData {
  id: number;
  name: string;
  brand: BrandData;
  scale: ScaleData;
  kit_number: string;
  difficulty: 10 | 20 | 30 | 40 | 50;
  box_image: {
    small: string;
  };
}

interface ListResponseData {
  count: number;
  paginate_by: number;
  previous: string | null;
  next: string | null;
  results: ModelKitData[];
}

export const getModelKit = async (id: number): Promise<ModelKitData> => {
  const cart = await get<ModelKitData>(`kits/kit/${id}/`);
  return cart!;
};

export const listModelKits = async (query: ListQueryParameters): Promise<ListResponseData> => {
  const params = Object.entries(query).map((entry: [string, string | number]): [string, string] => {
    const [key, value] = entry;
    return [key, value.toString()];
  });
  const responseData = await get<ListResponseData>('kits/kit/', params);
  return responseData!;
};

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
