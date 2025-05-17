import {get, post} from '@/data/api-client';

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

export const createBrand = async (name: string): Promise<BrandData> => {
  const brand = await post<BrandData, {name: string}>('kits/brand/', {name});
  return brand!;
};
