import React from 'react';
import {createRoot} from 'react-dom/client';
import {IntlProvider} from 'react-intl';
import {BrowserRouter as Router} from 'react-router-dom';

import {getCartDetails} from '../data/shop/cart';
import {getIntlProviderProps} from '../i18n';
import {CartDetail, CartProduct, TopbarCart} from './components/Cart';
import {Checkout} from './components/Checkout';
import {camelize} from './components/Checkout/utils';
import Shop from './components/Shop';
import {CartStore} from './store';

const getDataFromScript = scriptId => {
  const node = document.getElementById(scriptId);
  if (!node) return null;
  const data = JSON.parse(node.innerText);
  return data ? camelize(data) : null;
};

const bindAddToCartForm = (form, cartStore) => {
  if (!form) return;
  form.addEventListener('submit', event => {
    event.preventDefault();
    const {productId, amount} = Object.fromEntries(new FormData(form));
    cartStore.addProduct({
      product: parseInt(productId),
      amount: parseInt(amount),
    });
  });
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

    // find portal nodes
    const node = document.getElementById('react-cart');
    const detailNode = document.getElementById('react-cart-detail');

    // set up cart action handlers on list/overview pages
    const initCartActions = cartStore => {
      const products = document.getElementsByClassName('product-card');

      for (let product of products) {
        const {product: id, stock} = product.dataset;
        const reactNode = product.querySelector('.react-cart-actions');

        createRoot(reactNode).render(
          <IntlProvider {...intlProps}>
            <CartProduct store={cartStore} productId={id} hasStock={parseInt(stock) > 0} />
          </IntlProvider>,
        );
      }
    };

    const {checkoutPath = '', cartDetailPath = ''} = node?.dataset || {};

    try {
      this.reactRoot.render(
        <IntlProvider {...intlProps}>
          <Shop topbarCartNode={node} checkoutPath={checkoutPath} cartDetailPath={cartDetailPath} />
        </IntlProvider>,
      );

      // legacy
      const cart = await getCartDetails();
      let cartStore = new CartStore(cart);
      initCartActions(cartStore);
      this.initCheckout(intlProps, cartStore);

      if (detailNode) {
        const {checkoutPath: detailCheckoutPath, indexPath} = detailNode.dataset;
        createRoot(detailNode).render(
          <IntlProvider {...intlProps}>
            <CartDetail store={cartStore} checkoutPath={detailCheckoutPath} indexPath={indexPath} />
          </IntlProvider>,
        );
      }

      const productOrder = document.querySelector('.product .order-button');
      bindAddToCartForm(productOrder, cartStore);
    } catch (err) {
      console.error('Error retrieving cart', err);
      // TODO render error page/modal/toast
    }
  }

  static initCheckout(intlProps, cartStore) {
    const node = document.getElementById('react-checkout');
    if (!node) return;
    const {path: basePath, csrftoken, confirmPath} = node.dataset;
    const root = createRoot(node);

    // read user profile data from DOM, if user is not authenticated, this will be
    // an empty object
    const userProfileScript = document.getElementById('user_profile_data');
    const user = JSON.parse(userProfileScript.innerText);

    // read backend data and validation errors
    const checkoutData = getDataFromScript('checkout-data');
    const validationErrors = getDataFromScript('checkout-errors');
    const orderDetails = getDataFromScript('order-details');

    // mount and render the checkout component in the DOM
    root.render(
      <IntlProvider {...intlProps}>
        <Router basename={basePath}>
          <Checkout
            csrftoken={csrftoken}
            confirmPath={confirmPath}
            user={user}
            cartStore={cartStore}
            checkoutData={checkoutData}
            orderDetails={orderDetails}
            validationErrors={validationErrors}
          />
        </Router>
      </IntlProvider>,
    );
  }
}
