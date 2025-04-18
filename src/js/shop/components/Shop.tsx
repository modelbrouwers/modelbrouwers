import {createPortal} from 'react-dom';
import useAsync from 'react-use/esm/useAsync';

import {getCartDetails} from '@/data/shop/cart';

import {CartProduct} from '../data';
import {TopbarCart} from './Cart';

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
  const {
    loading,
    value: cart,
    error,
  } = useAsync(async () => {
    const cartData = await getCartDetails();
    return {
      ...cartData,
      products: cartData.products.map(cp => new CartProduct(cp)),
    };
  }, []);

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
