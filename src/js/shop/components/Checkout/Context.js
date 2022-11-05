import React from "react";

const CheckoutContext = React.createContext({
    validationErrors: null,
    customer: null,
    deliveryAddress: null,
    billingAddress: null,
});

CheckoutContext.displayName = "CheckoutContext";

export { CheckoutContext };
