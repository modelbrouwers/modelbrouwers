/**
 * Render the shopping cart in the body of the page
 */
import {observer} from 'mobx-react';
import React from 'react';
import {FormattedMessage} from 'react-intl';

import type {CartStore} from '@/shop/store';

import {CartProductRow, CartProductsTableHeader, Column} from './CartProductsTable';

const BODY_CART_COLUMNS: Column[] = [
  'image',
  'productName',
  'quantity',
  'unitPrice',
  'totalHeader',
];

export interface PaymentCartOverviewProps {
  store: CartStore;
}

const PaymentCartOverview: React.FC<PaymentCartOverviewProps> = ({store: cart}) => {
  if (!cart.products.length) {
    return (
      <FormattedMessage
        description="Payment page: cart empty"
        defaultMessage="Your cart is empty!"
      />
    );
  }

  return (
    <div className="cart cart--full">
      <table className="cart-products-table">
        <CartProductsTableHeader columns={BODY_CART_COLUMNS} />
        <tbody>
          {cart.products.map(cp => (
            // TODO: add remove option
            <CartProductRow
              key={cp.id}
              columns={BODY_CART_COLUMNS}
              cartProduct={cp}
              amountEditable
              onChangeAmount={async (_, newAmount) => {
                const delta = newAmount - cp.amount;
                cart.changeAmount(cp.product.id, delta);
              }}
            />
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default observer(PaymentCartOverview);
