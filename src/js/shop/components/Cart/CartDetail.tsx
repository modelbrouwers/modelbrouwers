import {FormattedMessage, type MessageDescriptor} from 'react-intl';

import {CartProduct} from '@/shop/data';

import Price from './Price';
import {AmountControls} from './ProductControls';
import ProductImage from './ProductImage';
import messages from './messages';
import {getTotal} from './utils';

const HEADERS: MessageDescriptor[] = [
  messages.image,
  messages.productName,
  messages.model,
  messages.quantity,
  messages.unitPrice,
  messages.totalHeader,
];

export interface CartDetailProps {
  checkoutPath: string;
  indexPath: string;
  cartProducts: CartProduct[];
  onChangeAmount: (cartProductId: number, newAmount: number) => Promise<void>;
}

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

    <table className="cart-detail__table">
      <thead className="cart-detail__thead">
        <tr>
          {HEADERS.map((header, i) => (
            <FormattedMessage {...header} tagName="th" key={i} />
          ))}
        </tr>
      </thead>
      <tbody className="cart-detail__tbody">
        {cartProducts.map(cp => (
          <tr key={cp.id}>
            <td>
              <ProductImage product={cp.product} className="cart-detail__image" />
            </td>
            <td>
              <a href="#" className="cart-detail__name">
                {cp.product.name}
              </a>
            </td>
            <td>
              <p className="cart-detail__model">{cp.product.model_name}</p>
            </td>
            <td className="cart-detail__quantity">
              <AmountControls
                currentAmount={cp.amount}
                onChangeAmount={(newAmount: number) => onChangeAmount(cp.id, newAmount)}
              />
            </td>
            <td>
              <p className="cart-detail__unit-price">
                <Price value={cp.product.price} />
              </p>
            </td>
            <td>
              <p className="cart-detail__product-total">
                <Price value={cp.total} />
              </p>
            </td>
          </tr>
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
