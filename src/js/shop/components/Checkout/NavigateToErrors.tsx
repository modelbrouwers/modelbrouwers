import {Navigate} from 'react-router';

import {useCheckoutContext} from './Context';

/**
 * Navigate to the first route that has validation errors set by the backend.
 */
const NavigateToErrors: React.FC = () => {
  const {hasDeliveryDetailsErrors, hasPaymentErrors} = useCheckoutContext();
  const navigateTo = hasDeliveryDetailsErrors ? '/address' : hasPaymentErrors ? '/payment' : '/';
  return <Navigate to={navigateTo} />;
};

export default NavigateToErrors;
