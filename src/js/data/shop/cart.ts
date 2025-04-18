import {CrudConsumer, CrudConsumerObject} from 'consumerjs';

import {API_ROOT} from '@//constants.js';
import {get} from '@/data/api-client';

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

class CartProduct extends CrudConsumerObject {}

export class CartProductConsumer extends CrudConsumer {
  constructor(endpoint = `${API_ROOT}api/v1/shop/cart-product`, objectClass = CartProduct) {
    super(endpoint, objectClass);
  }

  getCartProduct(id) {
    return this.get(`/${id}`);
  }

  getCartProducts(params) {
    return this.get(`/`, params);
  }

  /**
   * Add product to cart
   * @param {Object} data
   * @property {Number} product - id of the product
   * @property {Number} cart - id of the cart
   * @property {Number} amount - amount of products
   * @returns {Promise}
   */
  addProduct(data) {
    return this.post('/', data);
  }

  /**
   * Completely remove product from cart
   * @param id
   */
  removeProduct(id) {
    return this.delete(`/${id}`);
  }

  updateAmount(id, amount) {
    return this.patch(`/${id}/`, {amount});
  }
}
