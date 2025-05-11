import {FormattedMessage} from 'react-intl';

import type {CartProduct} from '@/shop/data';

import {CartProductRow, CartProductsTableHeader, type Column} from './CartProductsTable';
import Price from './Price';
import {getTotal} from './utils';

export interface CartDetailProps {
  checkoutPath: string;
  indexPath: string;
  cartProducts: CartProduct[];
  onChangeAmount: (cartProductId: number, newAmount: number) => Promise<void>;
  shippingCosts: number;
}

const CART_DETAIL_COLUMNS: Column[] = [
  'image',
  'productName',
  'model',
  'quantity',
  'unitPrice',
  'totalHeader',
];

/**
 * Display the contents of the shopping cart.
 */
const CartDetail: React.FC<CartDetailProps> = ({
  cartProducts,
  onChangeAmount,
  shippingCosts = 0,
  checkoutPath,
  indexPath,
}) => (
  <div className="cart-detail">
    <h2 className="cart-detail__page-header">
      <FormattedMessage description="Shopping cart title" defaultMessage="Shopping cart" />
    </h2>

    <table className="cart-products-table">
      <CartProductsTableHeader columns={CART_DETAIL_COLUMNS} />
      <tbody>
        {cartProducts.map(cp => (
          <CartProductRow
            key={cp.id}
            columns={CART_DETAIL_COLUMNS}
            cartProduct={cp}
            onChangeAmount={onChangeAmount}
          />
        ))}
      </tbody>
    </table>

    {/*TODO: Calculate sub-total and taxes*/}
    <div className="cart-detail__row">
      <div className="cart-detail__totals">
        <div className="cart-detail__inner">
          <h4>
            <FormattedMessage id="shop.cart.detail.title.cart.total" defaultMessage="Cart total" />
          </h4>

          {/* TODO */}
          <PriceKeyValue price={0}>
            <FormattedMessage id="shop.cart.detail.cart.subtotal" defaultMessage="Sub-total" />
          </PriceKeyValue>

          {/* TODO */}
          <PriceKeyValue price={0}>
            <FormattedMessage id="shop.cart.detail.cart.taxes" defaultMessage="Taxes" />
          </PriceKeyValue>

          {shippingCosts ? (
            <PriceKeyValue price={shippingCosts}>
              <FormattedMessage
                description="Cart detail: shipping costs label"
                defaultMessage="Shipping costs"
              />
            </PriceKeyValue>
          ) : null}

          <PriceKeyValue price={getTotal(cartProducts) + shippingCosts}>
            <FormattedMessage id="shop.cart.detail.cart.total" defaultMessage="Total" />
          </PriceKeyValue>
        </div>

        <div className="cart-detail__action-row">
          <a href={indexPath} className="button button--blue">
            <FormattedMessage
              description="Button back to webshop homepage"
              defaultMessage="Continue shopping"
            />
          </a>
          <a href={checkoutPath} className="button button--blue">
            <FormattedMessage description="Button to webshop checkout" defaultMessage="Checkout" />
          </a>
        </div>
      </div>
    </div>
  </div>
);

interface PriceKeyValueProps {
  children: React.ReactNode;
  price: number;
}

const PriceKeyValue: React.FC<PriceKeyValueProps> = ({children, price}) => (
  <div className="key-value key-value--stretch-mobile">
    <span className="key-value__label key-value__label--plain">{children}</span>
    <span className="key-value__text">
      <Price value={price} />
    </span>
  </div>
);

export default CartDetail;
