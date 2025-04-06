import React, { Component } from "react";
import PropTypes from "prop-types";
import { observer } from "mobx-react";
import classNames from "classnames";
import { FormattedMessage } from "react-intl";

import ProductImage from "./ProductImage";

@observer
export default class TopbarCart extends Component {
  static propTypes = {
    store: PropTypes.object.isRequired,
    checkoutPath: PropTypes.string.isRequired,
    cartDetailPath: PropTypes.string.isRequired,
  };

  constructor(props) {
    super(props);

    this.state = { expanded: false };
  }

  expandCart = () => {
    this.setState({ expanded: true });
  };

  collapseCart = () => {
    this.setState({ expanded: false });
  };

  render() {
    const { store: cart, checkoutPath, cartDetailPath } = this.props;
    const { expanded } = this.state;
    const containerClasses = classNames("cart__container", {
      "cart__container--expanded": expanded,
    });

    return (
      <div className="cart__row">
        <div
          className={containerClasses}
          onMouseOver={this.expandCart}
          onMouseOut={this.collapseCart}
        >
          <div className="cart__box">
            <div className="cart__inner">
              <i className="fa fa-shopping-basket cart__icon" />
              <div className="cart__info">
                <div className="cart__items">
                  <FormattedMessage
                    id="shop.cart.topbar.item.count"
                    defaultMessage={`{count, number} {count, plural, one {item} other {items}}`}
                    values={{ count: cart.amount }}
                  />
                </div>
                <div className="cart__price">&euro; {cart.total}</div>
              </div>
            </div>
          </div>
          <div className="cart__menu">
            <div className="cart__actions">
              <a href={cartDetailPath} className="button button--blue">
                <FormattedMessage
                  id="shop.cart.topbar.view.cart"
                  defaultMessage="View cart"
                />
              </a>
              <a href={checkoutPath} className="button button--blue">
                <FormattedMessage
                  id="shop.cart.topbar.checkout"
                  defaultMessage="Checkout"
                />
              </a>
            </div>
            <ul className="cart__products">
              {cart.products.map((cp, i) => (
                <li key={cp.id} className="cart-product cart-product--small">
                  <div className="cart-product__image">
                    <ProductImage product={cp.product} />
                  </div>
                  <p className="cart-product__name">{cp.product.name}</p>
                  <div className="cart-product__amount">{cp.amount}</div>
                  <div className="cart-product__price">
                    &euro; {cp.totalStr}
                  </div>
                  <div
                    className="cart-product__remove"
                    onClick={() => cart.removeProduct(cp.id)}
                  >
                    <i className="fa fa-close" />
                  </div>
                </li>
              ))}
            </ul>

            {cart.shippingCosts ? (
              <div
                className="cart__shipping text-right"
                style={{ padding: "10px" }}
              >
                Shipping: &euro; {cart.shippingCosts}
              </div>
            ) : null}
          </div>
        </div>
      </div>
    );
  }
}
