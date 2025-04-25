import {FormattedMessage, useIntl} from 'react-intl';
import {Route, Routes, useLocation} from 'react-router-dom';

import {Account, Confirmation, Delivery, Payment} from '.';
import CheckoutIndex from './CheckoutIndex';
import {useCheckoutContext} from './Context';
import NavLink from './NavLink';
import NavigateToErrors from './NavigateToErrors';
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

  const addressStepErrors = validateAddressDetails(deliveryDetails, intl);
  const addressStepValid = pathname !== '/' && Object.keys(addressStepErrors).length === 0;

  return (
    <div className="nav-wrapper">
      <h2 className="nav-wrapper__title">
        <FormattedMessage description="Checkout header" defaultMessage="Checkout" />
      </h2>

      <div className="nav-wrapper__content">
        <Routes>
          <Route path="" Component={CheckoutIndex} />
          <Route path="account" Component={Account} />
          <Route path="address" Component={Delivery} />
          <Route path="payment" Component={Payment} />
          {/* This is a backend URL - if there are validation errors, it renders
              the response at this URL. */}
          <Route path="confirm" Component={NavigateToErrors} />
          {/* Success page */}
          <Route path="confirmation" Component={Confirmation} />
        </Routes>
      </div>

      <nav className="nav-wrapper__nav">
        <ul className="navigation">
          <li className="navigation__item">
            <NavLink to="account" isEnabled={!isAuthenticated}>
              <FormattedMessage description="Tab: account" defaultMessage="Account" />
            </NavLink>
          </li>
          <li className="navigation__item">
            <NavLink to="address" isEnabled hasErrors={hasDeliveryDetailsErrors}>
              <FormattedMessage description="Tab: address" defaultMessage="Address" />
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

export default Checkout;
