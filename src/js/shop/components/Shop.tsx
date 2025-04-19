import {useCallback, useEffect} from 'react';
import {createPortal} from 'react-dom';
import useAsync from 'react-use/esm/useAsync';
import {ImmerReducer, useImmerReducer} from 'use-immer';

import {CartData, CartProductData, getCartDetails} from '@/data/shop/cart';

import {CartProduct} from '../data';
import {CartDetail, TopbarCart} from './Cart';
import ProductControls from './Cart/ProductControls';

export interface CatalogueProduct {
  id: number;
  stock: number;
  controlsNode: HTMLDivElement;
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
    }
  | {
      type: 'CART_PRODUCT_AMOUNT_UPDATED';
      payload: {
        id: number;
        cartProductData: CartProductData | null;
      };
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
    case 'CART_PRODUCT_AMOUNT_UPDATED': {
      if (draft.cart === null) throw new Error('No cart in state!');
      const {id, cartProductData} = action.payload;
      const existingIndex = draft.cart.products.findIndex(cp => cp.id === id);

      if (cartProductData === null) {
        draft.cart.products.splice(existingIndex, 1);
      } else {
        draft.cart.products[existingIndex].amount = cartProductData.amount;
      }

      break;
    }
    default: {
      const exhaustiveCheck: never = type;
      throw new Error(`Unexpected action type ${exhaustiveCheck}`);
    }
  }
};

export interface ShopProps {
  topbarCartNode: HTMLDivElement | null;
  productsOnPage: CatalogueProduct[];
  addProductNode: HTMLFormElement | null;
  cartDetailNode: HTMLDivElement | null;
  cartDetailPath: string;
  checkoutPath: string;
  indexPath: string;
  onAddToCart: (productId: number, amount?: number) => Promise<CartProductData>;
  onChangeAmount: (cartProductId: number, amount: number) => Promise<CartProductData | null>;
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
  addProductNode,
  cartDetailNode,
  cartDetailPath,
  checkoutPath,
  indexPath,
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

  useAddProductFormSubmit(addProductNode, cart?.products, onAddToCart, onChangeAmount, dispatch);

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
            onRemoveProduct={async (cartProductId: number) => {
              const cartProductData = await onChangeAmount(cartProductId, 0);
              dispatch({
                type: 'CART_PRODUCT_AMOUNT_UPDATED',
                payload: {
                  id: cartProductId,
                  cartProductData,
                },
              });
            }}
          />,
          topbarCartNode,
        )}
      {productsOnPage.map(({id, stock, controlsNode}, idx) =>
        createPortal(
          <ProductControls
            currentAmount={cart.products.find(cp => cp.product.id === id)?.amount ?? 0}
            hasStock={stock > 0}
            onAddProduct={async () => {
              const cartProductData = await onAddToCart(id);
              dispatch({
                type: 'PRODUCT_ADDED',
                payload: new CartProduct(cartProductData),
              });
            }}
            onChangeAmount={async newAmount => {
              // you can only change the amount if it's already in your cart, so we are
              // guaranteed to have a hit
              const cartProductId = cart.products.find(cp => cp.product.id === id)!.id;
              const cartProductData = await onChangeAmount(cartProductId, newAmount);
              dispatch({
                type: 'CART_PRODUCT_AMOUNT_UPDATED',
                payload: {
                  id: cartProductId,
                  cartProductData,
                },
              });
            }}
          />,
          controlsNode,
          `${id}-${idx}`,
        ),
      )}
      {cartDetailNode &&
        createPortal(
          <CartDetail
            checkoutPath={checkoutPath}
            indexPath={indexPath}
            cartProducts={cart.products}
            onChangeAmount={async (cartProductId: number, newAmount: number) => {
              const cartProductData = await onChangeAmount(cartProductId, newAmount);
              dispatch({
                type: 'CART_PRODUCT_AMOUNT_UPDATED',
                payload: {
                  id: cartProductId,
                  cartProductData,
                },
              });
            }}
          />,
          cartDetailNode,
        )}
    </>
  );
};

const useAddProductFormSubmit = (
  addProductNode: ShopProps['addProductNode'],
  currentProducts: CartProduct[] | undefined = [],
  onAddToCart: ShopProps['onAddToCart'],
  onChangeAmount: ShopProps['onChangeAmount'],
  dispatch: React.Dispatch<DispatchAction>,
) => {
  const onAddProductFormSubmit = useCallback(
    async (event: SubmitEvent) => {
      event.preventDefault();
      const formData = new FormData(event.target as HTMLFormElement);

      const productId = parseInt(formData.get('productId') as string);
      const amount = parseInt(formData.get('amount') as string);

      const existingCartProduct = currentProducts.find(cp => cp.product.id === productId);
      if (!existingCartProduct) {
        const cartProductData = await onAddToCart(productId, amount);
        dispatch({
          type: 'PRODUCT_ADDED',
          payload: new CartProduct(cartProductData),
        });
      } else {
        const newAmount = existingCartProduct.amount + amount;
        const cartProductData = await onChangeAmount(existingCartProduct.id, newAmount);
        dispatch({
          type: 'CART_PRODUCT_AMOUNT_UPDATED',
          payload: {
            id: existingCartProduct.id,
            cartProductData,
          },
        });
      }
    },
    [onAddToCart, onChangeAmount, dispatch, currentProducts],
  );

  useEffect(() => {
    if (!addProductNode) return;
    addProductNode.addEventListener('submit', onAddProductFormSubmit);
    return () => {
      addProductNode.removeEventListener('submit', onAddProductFormSubmit);
    };
  }, [addProductNode, onAddProductFormSubmit]);
};

export default Shop;
