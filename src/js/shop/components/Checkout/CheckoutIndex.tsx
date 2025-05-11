import {Navigate} from 'react-router';

import {useCheckoutContext} from './Context';

const CheckoutIndex: React.FC = () => {
  const {isAuthenticated} = useCheckoutContext();
  return <Navigate to={isAuthenticated ? 'delivery' : 'account'} />;
};

export default CheckoutIndex;
