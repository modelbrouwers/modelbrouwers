import {createPortal} from 'react-dom';
import useAsync from 'react-use/esm/useAsync';
import {ImmerReducer, useImmerReducer} from 'use-immer';

import {CartData, CartProductData, getCartDetails} from '@/data/shop/cart';

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
  onAddToCart: (productId: number) => Promise<CartProductData>;
  onChangeAmount: (productId: number, amount: 1 | -1) => void;
}

interface ShopState {
  cart: null | (Pick<CartData, 'id' | 'user'> & {products: CartProduct[]});
}

type DispatchAction =
  | {
      type: 'CART_LOADED';
      payload: ShopState['cart'];
    }
  | {
      type: 'PRODUCT_ADDED';
      payload: CartProduct;
    };

const reducer: ImmerReducer<ShopState, DispatchAction> = (
  draft: ShopState,
  action: DispatchAction,
) => {
  const {type} = action;
  switch (type) {
    case 'CART_LOADED': {
      draft.cart = action.payload;
      break;
    }
    case 'PRODUCT_ADDED': {
      if (draft.cart === null) throw new Error('No cart in state!');
      draft.cart.products.push(action.payload);
      break;
    }
    default: {
      const exhaustiveCheck: never = type;
      throw new Error(`Unexpected action type ${exhaustiveCheck}`);
    }
  }
};

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
  const [{cart}, dispatch] = useImmerReducer<ShopState, DispatchAction>(reducer, {
    cart: null,
  });

  const {loading, error} = useAsync(async () => {
    const cartData = await getCartDetails();
    const cart = {
      ...cartData,
      products: cartData.products.map(cp => new CartProduct(cp)),
    };
    dispatch({type: 'CART_LOADED', payload: cart});
  }, []);

  if (error) throw error;
  if (loading || cart === null) return null;

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
              onChangeAmount={amount => {
                onChangeAmount(id, amount);
              }}
              onAddProduct={async () => {
                const cartProductData = await onAddToCart(id);
                dispatch({
                  type: 'PRODUCT_ADDED',
                  payload: new CartProduct(cartProductData),
                });
              }}
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
