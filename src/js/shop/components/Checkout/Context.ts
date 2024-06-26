import React from "react";

import { AddressDetails } from "./types";

export type CheckoutContextType = {
  [K in keyof AddressDetails]: AddressDetails[K] | null;
} & {
  // TODO -> recursive structure where every node can be an error list from DRF
  validationErrors: unknown;
};

const CheckoutContext = React.createContext<CheckoutContextType>({
  validationErrors: null,
  customer: null,
  deliveryAddress: null,
  billingAddress: null,
});

CheckoutContext.displayName = "CheckoutContext";

export { CheckoutContext };
