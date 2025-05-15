import {get, post} from '@/data/api-client';

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

export const getModelKit = async (id: number): Promise<ModelKitData> => {
  const cart = await get<ModelKitData>(`kits/kit/${id}/`);
  return cart!;
};

interface ListResponseData {
  count: number;
  paginate_by: number;
  previous: string | null;
  next: string | null;
  results: ModelKitData[];
}

export const listModelKits = async (query: ListQueryParameters): Promise<ListResponseData> => {
  const params = Object.entries(query).map((entry: [string, string | number]): [string, string] => {
    const [key, value] = entry;
    return [key, value.toString()];
  });
  const responseData = await get<ListResponseData>('kits/kit/', params);
  return responseData!;
};

interface CreateKitData extends Pick<ModelKitData, 'name' | 'kit_number' | 'difficulty'> {
  box_image_uuid: string;
}

interface CreateKitResponseData extends ModelKitData {
  url_kitreviews: string;
}

export const createModelKit = async (data: CreateKitData): Promise<CreateKitResponseData> => {
  const kit = await post<CreateKitResponseData, CreateKitData>('kits/kit/', data);
  return kit!;
};
