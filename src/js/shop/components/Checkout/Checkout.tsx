import classNames from 'classnames';
import get from 'lodash/get';
import set from 'lodash/set';
import unset from 'lodash/unset';
import {useEffect} from 'react';
import {FormattedMessage, useIntl} from 'react-intl';
import {Navigate, NavLink as RRNavLink, Route, Routes, useLocation} from 'react-router-dom';
import {useImmerReducer} from 'use-immer';

import {Account, Confirmation, Delivery, Payment} from '.';
import FAIcon from '../../../components/FAIcon';
import CheckoutIndex from './CheckoutIndex';
import {useCheckoutContext} from './Context';
import {EMPTY_ADDRESS} from './constants';
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

const initialState = {
  customer: {
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
  },
  deliveryAddress: EMPTY_ADDRESS,
  billingAddress: null, // same as delivery address
  addressStepValid: false,
};

const reducer = (draft, action) => {
  switch (action.type) {
    case 'CHECK_ADDRESS_VALIDITY': {
      const {intl} = action.payload;
      const errors = validateAddressDetails(
        {
          customer: draft.customer,
          deliveryAddress: draft.deliveryAddress,
          billingAddress: draft.billingAddress,
        },
        intl,
      );
      draft.addressStepValid = Object.keys(errors).length === 0;
      break;
    }
    default: {
      throw new Error(`Unknown action type: ${action.type}`);
    }
  }
};

const checkHasValidationErrors = (validationErrors, errorKey) => {
  const keys = !Array.isArray(errorKey) ? [errorKey] : errorKey;
  if (!validationErrors) return false;
  for (const key of keys) {
    if (!validationErrors[key]) continue;
    const errors = Object.values(validationErrors[key]);
    if (errors.some(errorList => errorList && errorList.length > 0)) {
      return true;
    }
  }
  return false;
};

/**
 * Checkout
 */
const Checkout = ({orderDetails = null}) => {
  const intl = useIntl();
  const location = useLocation();
  const {isAuthenticated, validationErrors} = useCheckoutContext();

  const [state, dispatch] = useImmerReducer(reducer, initialState);

  useEffect(() => {
    if (location.pathname !== '/') {
      dispatch({type: 'CHECK_ADDRESS_VALIDITY', payload: {intl}});
    }
  }, [location, dispatch]);

  // re-arrange validation errors to match component structure
  const ERROR_MAP = {
    firstName: 'customer.firstName',
    lastName: 'customer.lastName',
    email: 'customer.email',
    phone: 'customer.phone',
  };
  for (const [from, to] of Object.entries(ERROR_MAP)) {
    const errors = get(validationErrors, from);
    if (!errors) continue;
    set(validationErrors, to, errors);
    unset(validationErrors, from);
  }

  const hasAddressValidationErrors = checkHasValidationErrors(validationErrors, [
    'customer',
    'deliveryAddress',
    'invoiceAddress',
  ]);
  const hasPaymentValidationErrors = checkHasValidationErrors(validationErrors, [
    'paymentMethod',
    'paymentMethodOptions',
    'cart',
  ]);
  let firstRouteWithErrors = '/';
  if (hasAddressValidationErrors) {
    firstRouteWithErrors = '/address';
  } else if (hasPaymentValidationErrors) {
    firstRouteWithErrors = '/payment';
  }

  return (
    <div className="nav-wrapper">
      <h2 className="nav-wrapper__title">
        <FormattedMessage description="Checkout header" defaultMessage="Checkout" />
      </h2>

      <div className="nav-wrapper__content">
        <Routes>
          <Route path="/" Component={CheckoutIndex} />
          <Route path="account" Component={Account} />
          <Route path="address" Component={Delivery} />
          <Route path="payment" Component={Payment} />
          {/* This is a backend URL - if there are validation errors, it renders
              the response at this URL. */}
          <Route path="confirm" element={<Navigate to={firstRouteWithErrors} />} />

          {/* Success page */}
          {orderDetails && (
            <Route
              path="confirmation"
              element={
                <Confirmation orderNumber={orderDetails.number} message={orderDetails.message} />
              }
            />
          )}
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
              hasErrors={hasAddressValidationErrors}
            >
              <FormattedMessage description="Tab: address" defaultMessage="Address" />
            </NavLink>
          </li>
          <li className="navigation__item">
            <NavLink
              to="payment"
              className={getActiveNavClassNames}
              enabled={state.addressStepValid}
              hasErrors={hasPaymentValidationErrors}
            >
              <FormattedMessage description="Tab: payment" defaultMessage="Payment" />
            </NavLink>
          </li>
          <li className="navigation__item">
            <NavLink to="confirmation" className={getActiveNavClassNames} enabled={!!orderDetails}>
              <FormattedMessage description="Tab: confirm" defaultMessage="Confirmation" />
            </NavLink>
          </li>
        </ul>
      </nav>
    </div>
  );
};

// Checkout.propTypes = {
//   orderDetails: PropTypes.shape({
//     number: PropTypes.string.isRequired,
//     message: PropTypes.string.isRequired,
//   }),
// };

export default Checkout;
