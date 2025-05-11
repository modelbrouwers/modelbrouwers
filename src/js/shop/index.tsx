import {Root, createRoot} from 'react-dom/client';
import {IntlConfig, IntlProvider} from 'react-intl';

import {setCsrfTokenValue} from '@/data/api-client';
import {createCartProduct, deleteCartProduct, patchCartProductAmount} from '@/data/shop/cart';
import {getIntlProviderProps} from '@/i18n.js';

import Shop from './components/Shop';

const getDataFromScript = (scriptId: string) => {
  const node = document.getElementById(scriptId);
  if (!node) return null;
  const data = JSON.parse(node.innerText);
  return data;
};

export default class Page {
  static reactRoot: Root;

  static async init() {
    try {
      const intlProviderProps = await getIntlProviderProps();
      // @ts-expect-error
      this.initCart(intlProviderProps);
    } catch (err) {
      console.log(err);
    }
  }

  static async initCart(intlProps: IntlConfig) {
    // find root node for our root component
    const rootNode = document.getElementById('react-root-shop')!;
    this.reactRoot = createRoot(rootNode);
    const {
      csrftoken = '',
      indexPath = '',
      cartDetailPath = '',
      checkoutPath = '',
      confirmPath = '',
    } = rootNode.dataset;
    setCsrfTokenValue(csrftoken as string);

    // find portal nodes
    const topbarCartNode = document.getElementById('react-topbar-cart') as HTMLDivElement | null;
    const cartDetailNode = document.getElementById('react-cart-detail') as HTMLDivElement | null;
    const addProductNode = document.querySelector(
      '.product .order-button',
    ) as HTMLFormElement | null;
    const checkoutNode = document.getElementById('react-checkout') as HTMLDivElement | null;

    const productsOnPage = Array.from(
      document.querySelectorAll<HTMLDivElement>('.product-card'),
    ).map(node => ({
      id: parseInt(node.dataset.product!),
      stock: parseInt(node.dataset.stock!),
      controlsNode: node.querySelector<HTMLDivElement>('.react-cart-actions')!,
    }));

    // read user profile data from DOM, if user is not authenticated, this will be
    // an empty object
    const userProfileScript = document.getElementById('user_profile_data');
    const user = userProfileScript ? JSON.parse(userProfileScript.innerText) : {};

    // read backend data and validation errors
    const checkoutData = getDataFromScript('checkout-data');
    const orderDetails = getDataFromScript('order-details');
    const validationErrors = getDataFromScript('checkout-errors');

    this.reactRoot.render(
      <IntlProvider {...intlProps}>
        <Shop
          topbarCartNode={topbarCartNode}
          productsOnPage={productsOnPage}
          addProductNode={addProductNode}
          cartDetailNode={cartDetailNode}
          checkoutNode={checkoutNode}
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
  }
}
