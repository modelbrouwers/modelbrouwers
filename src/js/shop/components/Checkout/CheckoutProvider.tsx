import {useCallback} from 'react';
import {type ImmerReducer, useImmerReducer} from 'use-immer';

import {CartProduct} from '@/shop/data';

import {CheckoutContext} from './Context';
import type {DeliveryDetails} from './types';

type CheckoutState = DeliveryDetails & {
  paymentMethod: number;
  paymentMethodOptions: null | Record<string, any>;
};

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
  cartId: number;
  cartProducts: CartProduct[];
  initialData: CheckoutState;
  confirmPath: string;
  // TODO
  validationErrors: unknown;
  children?: React.ReactNode;
}

const CheckoutProvider: React.FC<CheckoutProviderProps> = ({
  cartId,
  cartProducts,
  initialData,
  confirmPath,
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
        cartId,
        cartProducts,
        deliveryDetails: state,
        confirmPath,
        validationErrors,
        setDeliveryDetails,
      }}
    >
      {children}
    </CheckoutContext.Provider>
  );
};

export default CheckoutProvider;
