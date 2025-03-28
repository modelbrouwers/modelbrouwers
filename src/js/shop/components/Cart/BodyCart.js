/**
 * Render the shopping cart in the body of the page
 */
import { observer } from "mobx-react";
import React from "react";
import PropTypes from "prop-types";
import { FormattedMessage } from "react-intl";

import ProductImage from "./ProductImage";
import { DecrementButton, IncrementButton } from "./AmountButtons";

const CartProduct = ({ cartProduct, onChange }) => {
  const {
    product: { name, price, absoluteUrl },
    amount,
    totalStr,
  } = cartProduct;
  return (
    <div className="cart-product cart-product--full">
      <div className="cart-product__image">
        <ProductImage product={cartProduct.product} />
      </div>
      <div className="cart-product__name">
        <a href={absoluteUrl}>{name}</a>
      </div>
      <div className="cart-product__amount">
        <DecrementButton onClick={() => onChange(amount - 1)} />
        <input
          type="number"
          name="amount"
          value={amount}
          onChange={(event) => onChange(event.target.value)}
          min="0"
        />
        <IncrementButton onClick={() => onChange(amount + 1)} />
      </div>
      <div className="cart-product__price">&euro; {price}</div>
      <div className="cart-product__total">&euro; {totalStr}</div>
      {/* TODO: add remove option */}
    </div>
  );
};

CartProduct.propTypes = {
  cartProduct: PropTypes.shape({
    product: PropTypes.shape({
      name: PropTypes.string.isRequired,
      img: PropTypes.string,
      price: PropTypes.string.isRequired,
    }).isRequired,
    amount: PropTypes.number.isRequired,
  }).isRequired,
  onChange: PropTypes.func.isRequired,
};

const BodyCart = ({ store: cart }) => {
  const onChange = (cartProduct, newAmount) => {
    const delta = parseInt(newAmount, 10) - cartProduct.amount;
    cart.changeAmount(cartProduct.product.id, delta);
  };

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
      <div className="cart__product-list">
        <div className="cart-product cart-product--full cart-product--list-header">
          <div className="cart-product__image" />
          <div className="cart-product__name">
            <FormattedMessage
              description="Payment cart overview: name title"
              defaultMessage="product"
            />
          </div>
          <div className="cart-product__amount">
            <FormattedMessage
              description="Payment cart overview: amount title"
              defaultMessage="amount"
            />
          </div>
          <div className="cart-product__price">
            <FormattedMessage
              description="Payment cart overview: unit price title"
              defaultMessage="price"
            />
          </div>
          <div className="cart-product__total">
            <FormattedMessage
              description="Payment cart overview: total price title"
              defaultMessage="total"
            />
          </div>
        </div>

        {cart.products.map((cartProduct, index) => (
          <CartProduct
            key={`${cartProduct.product.id}-${index}`}
            cartProduct={cartProduct}
            onChange={(newAmount) => onChange(cartProduct, newAmount)}
          />
        ))}
      </div>

      {cart.shippingCosts ? (
        <div className="cart-product cart-product--full cart-product--list-header">
          <div className="cart-product__image" />
          <div className="cart-product__name">Shipping</div>
          <div className="cart-product__amount" />
          <div className="cart-product__price" />
          <div className="cart-product__total">&euro; {cart.shippingCosts}</div>
        </div>
      ) : null}
    </div>
  );
};

BodyCart.propTypes = {
  store: PropTypes.object.isRequired,
};

export default observer(BodyCart);
