import type {RouteObject} from 'react-router';

import Account from './Account';
import Checkout from './Checkout';
import CheckoutIndex from './CheckoutIndex';
import Confirmation from './Confirmation';
import Delivery from './Delivery';
import NavigateToErrors from './NavigateToErrors';
import Payment from './Payment';

const routes: RouteObject[] = [
  {
    Component: Checkout,
    children: [
      {
        path: '',
        index: true,
        Component: CheckoutIndex,
      },
      {
        path: 'account',
        Component: Account,
      },
      {
        path: 'address',
        Component: Delivery,
      },
      {
        path: 'payment',
        Component: Payment,
      },
      // This is a backend URL - if there are validation errors, it renders the response
      // at this URL.
      {
        path: 'confirm',
        Component: NavigateToErrors,
      },
      // Success page
      {
        path: 'confirmation',
        Component: Confirmation,
      },
    ],
  },
];

export default routes;
