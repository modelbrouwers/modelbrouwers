import type {CartProduct} from '@/shop/data';

export const getTotal = (cartProducts: CartProduct[]): number =>
  cartProducts.reduce((acc: number, cp: CartProduct) => acc + cp.total, 0);
