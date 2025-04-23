import classNames from 'classnames';
import {FormattedMessage, useIntl} from 'react-intl';
import {NavLink as RRNavLink, Route, Routes, useLocation} from 'react-router-dom';

import {Account, Confirmation, Delivery, Payment} from '.';
import FAIcon from '../../../components/FAIcon';
import CheckoutIndex from './CheckoutIndex';
import {useCheckoutContext} from './Context';
import NavigateToErrors from './NavigateToErrors';
import {validateAddressDetails} from './validation';

const getActiveNavClassNames = ({isActive, enabled = false}) =>
  classNames('navigation__link', {
    'navigation__link--active': isActive,
    'navigation__link--enabled': enabled,
  });

const NavLink = ({enabled = false, className, hasErrors = false, children, ...props}) => {
  const Container = enabled ? RRNavLink : 'span';
  const wrappedClassname = enabled
    ? ({isActive}) => className({isActive, enabled})
    : className({isActive: false, enabled});

  if (hasErrors) {
    children = (
      <span className="nav-link-wrapper">
        <span className="nav-link-wrapper__text">{children}</span>
        <span className="nav-link-wrapper__icon">
          <FAIcon icon="exclamation-circle" />
        </span>
      </span>
    );
  }

  return (
    <Container {...props} className={wrappedClassname}>
      {children}
    </Container>
  );
};

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
            <NavLink to="account" className={getActiveNavClassNames} enabled={!isAuthenticated}>
              <FormattedMessage description="Tab: account" defaultMessage="Account" />
            </NavLink>
          </li>
          <li className="navigation__item">
            <NavLink
              to="address"
              className={getActiveNavClassNames}
              enabled
              hasErrors={hasDeliveryDetailsErrors}
            >
              <FormattedMessage description="Tab: address" defaultMessage="Address" />
            </NavLink>
          </li>
          <li className="navigation__item">
            <NavLink
              to="payment"
              className={getActiveNavClassNames}
              enabled={addressStepValid}
              hasErrors={hasPaymentErrors}
            >
              <FormattedMessage description="Tab: payment" defaultMessage="Payment" />
            </NavLink>
          </li>
          <li className="navigation__item">
            <NavLink
              to="confirmation"
              className={getActiveNavClassNames}
              enabled={orderDetails !== null}
            >
              <FormattedMessage description="Tab: confirm" defaultMessage="Confirmation" />
            </NavLink>
          </li>
        </ul>
      </nav>
    </div>
  );
};

export default Checkout;
