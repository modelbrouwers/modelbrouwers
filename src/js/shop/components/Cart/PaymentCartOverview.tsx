/**
 * Render the shopping cart overview in the body of the page.
 */
import React from 'react';
import {FormattedMessage} from 'react-intl';

import type {CartProduct} from '@/shop/data';

import {CartProductRow, CartProductsTableHeader, Column} from './CartProductsTable';

const BODY_CART_COLUMNS: Column[] = [
  'image',
  'productName',
  'quantity',
  'unitPrice',
  'totalHeader',
];

export interface PaymentCartOverviewProps {
  cartProducts: CartProduct[];
  onChangeAmount: (cartProductId: number, newAmount: number) => Promise<void>;
}

const PaymentCartOverview: React.FC<PaymentCartOverviewProps> = ({
  cartProducts,
  onChangeAmount,
}) => {
  if (!cartProducts.length) {
    return (
      <FormattedMessage
        description="Payment page: cart empty"
        defaultMessage="Your cart is empty!"
      />
    );
  }

  return (
    <table className="cart-products-table">
      <CartProductsTableHeader columns={BODY_CART_COLUMNS} />
      <tbody>
        {cartProducts.map(cp => (
          // TODO: add remove option
          <CartProductRow
            key={cp.id}
            columns={BODY_CART_COLUMNS}
            cartProduct={cp}
            amountEditable
            onChangeAmount={onChangeAmount}
          />
        ))}
      </tbody>
    </table>
  );
};

export default PaymentCartOverview;
