import {createPortal} from 'react-dom';
import useAsync from 'react-use/esm/useAsync';

import {getCartDetails} from '@/data/shop/cart';

import {CartProduct} from '../data';
import {TopbarCart} from './Cart';
import ProductControls from './Cart/ProductControls';

export interface CatalogueProduct {
  id: number;
  stock: number;
  controlsNode: HTMLDivElement;
}

export interface ShopProps {
  topbarCartNode: HTMLDivElement | null;
  productsOnPage: CatalogueProduct[];
  cartDetailPath: string;
  checkoutPath: string;
  onAddToCart: (productId: number) => void;
  onChangeAmount: (productId: number, amount: 1 | -1) => void;
}

/**
 * Main component to manage everything web shop related.
 *
 * Takes care of tracking the shop state and renders all sub components into their
 * assigned portal nodes.
 */
const Shop: React.FC<ShopProps> = ({
  topbarCartNode,
  productsOnPage,
  cartDetailPath,
  checkoutPath,
  onAddToCart,
  onChangeAmount,
}) => {
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
      <>
        {productsOnPage.map(({id, stock, controlsNode}, idx) =>
          createPortal(
            <ProductControls
              currentAmount={cart.products.find(cp => cp.product.id === id)?.amount ?? 0}
              hasStock={stock > 0}
              onChangeAmount={amount => onChangeAmount(id, amount)}
              onAddProduct={() => onAddToCart(id)}
            />,
            controlsNode,
            `${id}-${idx}`,
          ),
        )}
      </>
    </>
  );
};

export default Shop;
