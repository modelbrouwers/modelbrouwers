// TODO: complete this
export interface User {}

export interface Product {
  id: number;
  name: string;
  image: string;
  price: number;
  // vat: number;
  // categories: unknown; // TODO
  model_name: string;
  // absoluteUrl: string;
  totalStr: string;
}

export interface CartProduct {
  // id: number | null;
  // cartId: number;
  product: Product | null;
  amount: number;
  totalStr: string;
}

export interface CartStore {
  id: number | null;
  user: User;
  products: CartProduct[];
  total: string;
}
