import React from 'react';
import {createRoot} from 'react-dom/client';
import {IntlProvider} from 'react-intl';

import {setCsrfTokenValue} from '@/data/api-client';

import {
  createCartProduct,
  deleteCartProduct,
  getCartDetails,
  patchCartProductAmount,
} from '../data/shop/cart';
import {getIntlProviderProps} from '../i18n';
import {CartDetail, TopbarCart} from './components/Cart';
import {Checkout} from './components/Checkout';
import {camelize} from './components/Checkout/utils';
import Shop from './components/Shop';
import {CartProduct} from './data';

const getDataFromScript = scriptId => {
  const node = document.getElementById(scriptId);
  if (!node) return null;
  const data = JSON.parse(node.innerText);
  return data ? camelize(data) : null;
};

export default class Page {
  static async init() {
    try {
      const intlProviderProps = await getIntlProviderProps();
      this.initCart(intlProviderProps);
    } catch (err) {
      console.log(err);
    }
  }

  static async initCart(intlProps) {
    // find root node for our root component
    const rootNode = document.getElementById('react-root-shop');
    this.reactRoot = createRoot(rootNode);
    const {csrftoken, indexPath, cartDetailPath, checkoutPath, confirmPath} = rootNode.dataset;
    setCsrfTokenValue(csrftoken);

    // find portal nodes
    const topbarCartNode = document.getElementById('react-topbar-cart');
    const cartDetailNode = document.getElementById('react-cart-detail');
    const addProductNode = document.querySelector('.product .order-button');
    const checkoutNode = document.getElementById('react-checkout');

    const productsOnPage = Array.from(document.querySelectorAll('.product-card')).map(node => ({
      id: parseInt(node.dataset.product),
      stock: parseInt(node.dataset.stock),
      controlsNode: node.querySelector('.react-cart-actions'),
    }));

    // read user profile data from DOM, if user is not authenticated, this will be
    // an empty object
    // TODO: camelize data and update components/type definitions
    const userProfileScript = document.getElementById('user_profile_data');
    const user = userProfileScript ? JSON.parse(userProfileScript.innerText) : {};

    // read backend data and validation errors
    const checkoutData = getDataFromScript('checkout-data');
    const orderDetails = getDataFromScript('order-details');
    const validationErrors = getDataFromScript('checkout-errors');

    try {
      this.reactRoot.render(
        <IntlProvider {...intlProps}>
          <Shop
            topbarCartNode={topbarCartNode}
            productsOnPage={productsOnPage}
            addProductNode={addProductNode}
            cartDetailNode={cartDetailNode}
            checkoutNode={checkoutNode}
            // TODO
            user={user}
            indexPath={indexPath}
            cartDetailPath={cartDetailPath}
            checkoutPath={checkoutPath}
            confirmPath={confirmPath}
            onAddToCart={async (cartId, productId, amount) =>
              await createCartProduct(cartId, productId, amount)
            }
            onChangeAmount={async (cartProductId, newAmount) => {
              if (newAmount > 0) {
                const updatedCartProduct = await patchCartProductAmount(cartProductId, newAmount);
                return updatedCartProduct;
              } else {
                await deleteCartProduct(cartProductId);
                return null;
              }
            }}
            checkoutData={checkoutData}
            orderDetails={orderDetails}
            validationErrors={validationErrors}
          />
        </IntlProvider>,
      );
    } catch (err) {
      console.error('Error retrieving cart', err);
      // TODO render error page/modal/toast
    }
  }
}
