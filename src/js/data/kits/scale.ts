import {get, post} from '@/data/api-client';

export interface ScaleData {
  id: number;
  scale: number;
  __str__: string;
}

export const listScales = async (): Promise<ScaleData[]> => {
  const responseData = await get<ScaleData[]>('kits/scale/');
  return responseData!;
};

const RE_SCALE = new RegExp('1[/:]([0-9]+)');

export const parseScale = (input: string): number => {
  const asNumber = Number(input);
  if (isNaN(asNumber)) {
    const match = RE_SCALE.exec(input);
    if (match) {
      return parseInt(match[1], 10);
    }
  }
  return asNumber;
};

export const createScale = async (scale: string): Promise<ScaleData> => {
  const numericScale = parseScale(scale);
  const brand = await post<ScaleData, {scale: number}>('kits/scale/', {scale: numericScale});
  return brand!;
};
