import {immerable} from 'immer';

import type {CartProductData, Product} from '@/data/shop/cart';

/**
 * Metadata/relation of a product in a cart.
 *
 * Implemented as a class for easy computed properties and single place to
 * calculate/define them.
 */
export class CartProduct {
  [immerable] = true;

  readonly id: number;
  readonly product: Product;
  public amount: number;

  constructor({id, product, amount}: CartProductData) {
    this.id = id;
    this.product = product;
    this.amount = amount;
  }

  public get total(): number {
    return this.product.price * this.amount;
  }
}
