import {createPortal} from 'react-dom';
import useAsync from 'react-use/esm/useAsync';

import {CartProduct} from '../data';
import {TopbarCart} from './Cart';

interface CartData {
  id: number;
  products: CartProduct[];
  user: {
    username: string;
    first_name: string;
    last_name: string;
    email: string;
    phone: string;
  } | null;
}

// Mock implementation for now
const fetchCart = async (): Promise<CartData> => {
  return {
    id: 42,
    user: null,
    products: [
      new CartProduct({
        id: 1,
        product: {
          id: 1,
          name: 'Product 1',
          image: 'https://loremflickr.com/400/300/cat',
          price: 3.78,
        },
        amount: 1,
      }),
      new CartProduct({
        id: 2,
        product: {
          id: 2,
          name: 'Product 2',
          image: 'https://loremflickr.com/400/300/cat',
          price: 2.07,
        },
        amount: 3,
      }),
    ],
  };
};

export interface ShopProps {
  topbarCartNode: HTMLDivElement | null;
  cartDetailPath: string;
  checkoutPath: string;
}

/**
 * Main component to manage everything web shop related.
 *
 * Takes care of tracking the shop state and renders all sub components into their
 * assigned portal nodes.
 */
const Shop: React.FC<ShopProps> = ({topbarCartNode, cartDetailPath, checkoutPath}) => {
  const {loading, value: cart, error} = useAsync(async () => await fetchCart(), []);
  if (error) throw error;
  if (loading || !cart) return null;

  return (
    <>
      {topbarCartNode &&
        createPortal(
          <TopbarCart
            cartDetailPath={cartDetailPath}
            checkoutPath={checkoutPath}
            cartProducts={cart.products}
            onRemoveProduct={console.log}
          />,
          topbarCartNode,
        )}
    </>
  );
};

export default Shop;
