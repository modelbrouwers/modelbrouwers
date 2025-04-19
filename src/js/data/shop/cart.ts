import {destroy, get, patch, post} from '@/data/api-client';

export interface Product {
  id: number;
  name: string;
  image: string;
  price: number;
  // vat: number;
  // categories: unknown; // TODO
  // model_name: string;
  // absoluteUrl: string;
  // totalStr: string;
}

export interface CartProductData {
  id: number;
  product: Product;
  amount: number;
  // cart: number; // cart ID
}

export interface CartData {
  id: number;
  products: CartProductData[];
  user: {
    username: string;
    first_name: string;
    last_name: string;
    email: string;
    phone: string;
  } | null;
}

export const getCartDetails = async (): Promise<CartData> => {
  const cart = await get<CartData>('shop/cart/');
  return cart!;
};

interface CreateCartProductData {
  cart: number;
  product: number;
  amount: number;
}

export const createCartProduct = async (
  cartId: number,
  productId: number,
  amount: number = 1,
): Promise<CartProductData> => {
  const cartProductData = await post<CartProductData, CreateCartProductData>('shop/cart-product/', {
    cart: cartId,
    product: productId,
    amount: amount,
  });
  return cartProductData!;
};

export const patchCartProductAmount = async (
  id: number,
  amount: number,
): Promise<CartProductData> => {
  const updatedCartProductData = await patch<CartProductData>(`shop/cart-product/${id}/`, {amount});
  return updatedCartProductData!;
};

export const deleteCartProduct = async (id: number): Promise<null> =>
  await destroy(`shop/cart-product/${id}/`);
