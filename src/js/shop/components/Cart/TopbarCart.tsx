import clsx from 'clsx';
import {useState} from 'react';
import {FormattedMessage} from 'react-intl';

import type {CartProduct} from '@/shop/data';

import Price from './Price';
import ProductImage from './ProductImage';
import {getTotal} from './utils';

export interface TopbarCartProps {
  cartProducts: CartProduct[];
  cartDetailPath: string;
  checkoutPath: string;
  onRemoveProduct: (id: number) => void;
  shippingCosts: number;
}

/**
 * @todo Clean up markup + CSS & ensure this is all accessible. The popout/dialog should
 * also be properly keyboard-navigation accessible.
 */
const TopbarCart: React.FC<TopbarCartProps> = ({
  cartProducts,
  cartDetailPath,
  checkoutPath,
  onRemoveProduct,
  shippingCosts = 0,
}) => {
  const [expanded, setExpanded] = useState(false);
  const totalProductCount: number = cartProducts.reduce(
    (acc: number, cp: CartProduct) => acc + cp.amount,
    0,
  );
  return (
    <div className="cart__row">
      <div
        className={clsx('cart__container', {
          'cart__container--expanded': expanded,
        })}
        onMouseOver={() => setExpanded(true)}
        onMouseOut={() => setExpanded(false)}
      >
        <div className="cart__box">
          <div className="cart__inner">
            <i className="fa fa-shopping-basket cart__icon" />
            <div className="cart__info">
              <div className="cart__items">
                <FormattedMessage
                  id="shop.cart.topbar.item.count"
                  defaultMessage={`{count, number} {count, plural, one {item} other {items}}`}
                  values={{count: totalProductCount}}
                />
              </div>
              <div className="cart__price">
                <Price value={getTotal(cartProducts) + shippingCosts} />
              </div>
            </div>
          </div>
        </div>
        <div className="cart__menu">
          <div className="cart__actions">
            <a href={cartDetailPath} className="button button--blue">
              <FormattedMessage id="shop.cart.topbar.view.cart" defaultMessage="View cart" />
            </a>
            <a href={checkoutPath} className="button button--blue">
              <FormattedMessage id="shop.cart.topbar.checkout" defaultMessage="Checkout" />
            </a>
          </div>

          <ul className="cart__products">
            {cartProducts.map(cp => (
              <TopbarCartProduct key={cp.id} cartProduct={cp} onRemove={onRemoveProduct} />
            ))}
          </ul>

          {shippingCosts ? (
            <div className="cart__shipping">
              <FormattedMessage
                description="TopbarCart shipping costs"
                defaultMessage="Shipping: <costs></costs>"
                values={{
                  costs: () => <Price value={shippingCosts} />,
                }}
              />
            </div>
          ) : null}
        </div>
      </div>
    </div>
  );
};

interface TopbarCartProductProps {
  cartProduct: CartProduct;
  onRemove: (id: number) => void;
}

const TopbarCartProduct: React.FC<TopbarCartProductProps> = ({
  cartProduct: {id, product, amount, total},
  onRemove,
}) => (
  <li className="cart-product cart-product--small">
    <div className="cart-product__image">
      <ProductImage product={product} />
    </div>
    <p className="cart-product__name">{product.name}</p>
    <div className="cart-product__amount">{amount}</div>
    <div className="cart-product__price">
      <Price value={total} />
    </div>
    <button type="button" className="cart-product__remove" onClick={() => onRemove(id)}>
      <i className="fa fa-close" aria-hidden="true" />
      <span className="sr-only">
        <FormattedMessage
          description="Cart: remove product button label"
          defaultMessage="Remove product ''{name}''"
          values={{
            name: product.name,
          }}
        />
      </span>
    </button>
  </li>
);

export default TopbarCart;
