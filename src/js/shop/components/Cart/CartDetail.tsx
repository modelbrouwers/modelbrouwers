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
          <div className="cart-detail__info-row">
            <span className="cart-detail__text">
              <FormattedMessage id="shop.cart.detail.cart.subtotal" defaultMessage="Sub-total" />
            </span>
            <span className="cart-detail__value">N/A</span>
          </div>
          <div className="cart-detail__info-row">
            <span className="cart-detail__text">
              <FormattedMessage id="shop.cart.detail.cart.taxes" defaultMessage="Taxes" />
            </span>
            <span className="cart-detail__value">N/A</span>
          </div>
          <div className="cart-detail__info-row">
            <span className="cart-detail__text">
              <FormattedMessage id="shop.cart.detail.cart.total" defaultMessage="Total" />
            </span>
            <span className="cart-detail__value">
              <Price value={getTotal(cartProducts)} />
            </span>
          </div>
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

export default CartDetail;
