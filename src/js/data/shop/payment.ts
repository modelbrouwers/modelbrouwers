import type {CountryOption} from '@/components/forms/CountryField';
import {get} from '@/data/api-client';

export interface PaymentMethod {
  id: number;
  name: string;
  logo: string;
  order: number;
}

export const listMethods = async (): Promise<PaymentMethod[]> => {
  const methods = await get<PaymentMethod[]>('shop/paymentmethod/');
  return methods!;
};

export interface IDealBank {
  id: number;
  name: string;
}

export const listIDealBanks = async (): Promise<IDealBank[]> => {
  const banks = await get<IDealBank[]>('shop/ideal_banks/');
  return banks!;
};

export interface ShippingsCostsResponse {
  weight: string;
  price: string;
}

export const calculateShippingCosts = async (
  cartId: number,
  country: CountryOption['value'],
): Promise<ShippingsCostsResponse> => {
  const shippingCosts = await get<ShippingsCostsResponse>('shop/shipping-costs/', {
    cart_id: cartId.toString(),
    country,
  });
  return shippingCosts!;
};
