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

interface CartProductData {
  id: number;
  product: Product;
  amount: number;
  // cart: number; // cart ID
}

/**
 * Metadata/relation of a product in a cart.
 *
 * Implemented as a class for easy computed properties and single place to
 * calculate/define them.
 */
export class CartProduct {
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
