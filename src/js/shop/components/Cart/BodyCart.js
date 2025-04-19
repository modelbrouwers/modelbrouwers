/**
 * Render the shopping cart in the body of the page
 */
import {observer} from 'mobx-react';
import PropTypes from 'prop-types';
import React from 'react';
import {FormattedMessage} from 'react-intl';

import {DecrementButton, IncrementButton} from './AmountButtons';
import {CartProductRow, CartProductsTableHeader} from './CartProductsTable';
import {AmountControls} from './ProductControls';
import ProductImage from './ProductImage';

const BODY_CART_COLUMNS = ['image', 'productName', 'quantity', 'unitPrice', 'totalHeader'];

const BodyCart = ({store: cart}) => {
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
              onChangeAmount={(cartProductId, newAmount) => {
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

BodyCart.propTypes = {
  store: PropTypes.object.isRequired,
};

export default observer(BodyCart);
