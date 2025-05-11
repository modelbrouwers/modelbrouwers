import {FormattedMessage, useIntl} from 'react-intl';
import {Outlet, useLocation} from 'react-router';
import useAsync from 'react-use/esm/useAsync';

import {calculateShippingCosts} from '@/data/shop/payment';

import {useCheckoutContext} from './Context';
import NavLink from './NavLink';
import {validateAddressDetails} from './validation';

/**
 * Checkout
 */
const Checkout: React.FC = () => {
  const intl = useIntl();
  const {pathname} = useLocation();
  const {
    isAuthenticated,
    deliveryDetails,
    hasDeliveryDetailsErrors,
    hasPaymentErrors,
    orderDetails,
  } = useCheckoutContext();

  // XXX: capture errors in a better way, but this may never crash the entire checkout
  // process!
  const shippingCostsError = useUpdateShippingCosts();
  if (shippingCostsError) {
    console.error(shippingCostsError);
  }

  const addressStepErrors = validateAddressDetails(deliveryDetails, intl);
  const addressStepValid = pathname !== '/' && Object.keys(addressStepErrors).length === 0;

  return (
    <div className="nav-wrapper">
      <h2 className="nav-wrapper__title">
        <FormattedMessage description="Checkout header" defaultMessage="Checkout" />
      </h2>

      <div className="nav-wrapper__content">
        <Outlet />
      </div>

      <nav className="nav-wrapper__nav">
        <ul className="navigation">
          <li className="navigation__item">
            <NavLink to="account" isEnabled={!isAuthenticated}>
              <FormattedMessage description="Tab: account" defaultMessage="Account" />
            </NavLink>
          </li>
          <li className="navigation__item">
            <NavLink to="delivery" isEnabled hasErrors={hasDeliveryDetailsErrors}>
              <FormattedMessage description="Tab: delivery" defaultMessage="Delivery" />
            </NavLink>
          </li>
          <li className="navigation__item">
            <NavLink to="payment" isEnabled={addressStepValid} hasErrors={hasPaymentErrors}>
              <FormattedMessage description="Tab: payment" defaultMessage="Payment" />
            </NavLink>
          </li>
          <li className="navigation__item">
            <NavLink to="confirmation" isEnabled={orderDetails !== null}>
              <FormattedMessage description="Tab: confirm" defaultMessage="Confirmation" />
            </NavLink>
          </li>
        </ul>
      </nav>
    </div>
  );
};

const useUpdateShippingCosts = () => {
  const {deliveryDetails, cartId, cartProducts, onChangeShippingCosts} = useCheckoutContext();

  // update the shipping costs when there are changes detected
  const {deliveryMethod, deliveryAddress} = deliveryDetails;
  const deliveryCountry = deliveryAddress?.country;
  const cartContents = JSON.stringify(cartProducts);

  const {error} = useAsync(async () => {
    // check whether we need to make a call in the first place
    if (deliveryMethod === 'pickup' || !cartId || !deliveryCountry) {
      onChangeShippingCosts({price: 0, weight: ''});
      return;
    } else {
      const costs = await calculateShippingCosts(cartId, deliveryCountry);
      onChangeShippingCosts(costs);
    }
  }, [, onChangeShippingCosts, cartId, cartContents, deliveryMethod, deliveryCountry]);

  return error;
};

export default Checkout;
