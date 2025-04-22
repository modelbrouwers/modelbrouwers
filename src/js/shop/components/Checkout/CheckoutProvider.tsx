import {useCallback} from 'react';
import {type ImmerReducer, useImmerReducer} from 'use-immer';

import {CartProduct} from '@/shop/data';

import {CheckoutContext} from './Context';
import type {DeliveryDetails, OrderDetails, PaymentDetails, UserData} from './types';

type CheckoutState = DeliveryDetails & PaymentDetails;

type DispatchAction = {
  type: 'SET_DELIVERY_DETAILS';
  payload: DeliveryDetails;
};

const reducer: ImmerReducer<CheckoutState, DispatchAction> = (
  draft: CheckoutState,
  action: DispatchAction,
) => {
  const {type} = action;
  switch (type) {
    case 'SET_DELIVERY_DETAILS': {
      Object.assign(draft, action.payload);
      break;
    }
    default: {
      const exhaustiveCheck: never = type;
      throw new Error(`Unexpected action type ${exhaustiveCheck}`);
    }
  }
};

export interface CheckoutProviderProps {
  user: UserData | null;
  cartId: number;
  cartProducts: CartProduct[];
  onChangeProductAmount: (cartProductId: number, newAmount: number) => Promise<void>;
  initialData: CheckoutState;
  confirmPath: string;
  orderDetails: OrderDetails;
  // TODO
  validationErrors: unknown;
  children?: React.ReactNode;
}

const CheckoutProvider: React.FC<CheckoutProviderProps> = ({
  user,
  cartId,
  cartProducts,
  onChangeProductAmount,
  initialData,
  confirmPath,
  orderDetails,
  validationErrors,
  children,
}) => {
  const [state, dispatch] = useImmerReducer<CheckoutState, DispatchAction>(reducer, initialData);

  const setDeliveryDetails = useCallback(
    (values: DeliveryDetails) => {
      dispatch({type: 'SET_DELIVERY_DETAILS', payload: values});
    },
    [dispatch],
  );

  console.log(state);

  return (
    <CheckoutContext.Provider
      value={{
        isAuthenticated: user !== null,
        cartId,
        cartProducts,
        onChangeProductAmount,
        deliveryDetails: state,
        confirmPath,
        setDeliveryDetails,
        orderDetails,
        validationErrors,
      }}
    >
      {children}
    </CheckoutContext.Provider>
  );
};

export default CheckoutProvider;
