// TODO: complete this
export interface User {
  username: string;
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
}

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
  id: number | null;
  product: Product;
  amount: number;
  cart: number; // ID
  total: string; // decimal serialized to string
}

export interface Cart {
  id: number;
  user: User;
  status: "open" | "processing" | "closed";
  products: CartProduct[];
  total: string; // decimal serialized to string
}
