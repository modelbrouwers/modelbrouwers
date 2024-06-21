import { useRef } from "react";
import { FormattedMessage } from "react-intl";
import { Formik, Form, FormikConfig } from "formik";

import { ErrorList } from "./FormFields";
import { BodyCart } from "../Cart";
import SelectPaymentMethod from "./SelectPaymentMethod";
import type { CartStore } from "@/shop/types";
import type { Address, DeliveryDetails } from "./types";

const addressToSerializerShape = (address: Address | null) => {
  if (!address) return null;
  return {
    street: address.street,
    number: address.number,
    postal_code: address.postalCode,
    city: address.city,
    country: address.country,
    company: address.company,
    chamber_of_commerce: address.chamberOfCommerce,
  };
};

interface IDealOptions {
  bank: number;
}

interface FormikValues {
  paymentMethod: string;
  paymentMethodOptions: {} | IDealOptions;
}

export interface PaymentProps {
  csrftoken: string;
  confirmPath: string;
  cartStore: CartStore;
  // TODO
  errors?: {
    cart?: any;
  };
  checkoutDetails: DeliveryDetails;
}

const Payment: React.FC<PaymentProps> = ({
  cartStore,
  csrftoken,
  confirmPath,
  errors,
  checkoutDetails,
}) => {
  const submitFormRef = useRef<HTMLFormElement>(null);

  const onFormikSubmit: FormikConfig<FormikValues>["onSubmit"] = ({
    paymentMethod,
    paymentMethodOptions,
  }) => {
    const checkoutData = {
      cart: cartStore.id,
      payment_method: parseInt(paymentMethod, 10),
      payment_method_options: paymentMethodOptions,
      first_name: checkoutDetails.customer.firstName,
      last_name: checkoutDetails.customer.lastName,
      email: checkoutDetails.customer.email,
      phone: checkoutDetails.customer.phone,
      delivery_address: addressToSerializerShape(
        checkoutDetails.deliveryAddress,
      ),
      invoice_address: addressToSerializerShape(checkoutDetails.billingAddress),
    };

    const form = submitFormRef.current;
    if (form === null) throw new Error("form ref should not be null");
    const checkoutDataInput = form.querySelector<HTMLInputElement>(
      'input[name="checkoutData"]',
    );
    checkoutDataInput!.value = JSON.stringify(checkoutData);
    form.submit();
  };

  const hasProducts = Boolean(cartStore.products.length);
  return (
    <>
      <Formik<FormikValues>
        initialValues={{
          paymentMethod: "",
          paymentMethodOptions: {},
        }}
        enableReinitialize
        onSubmit={onFormikSubmit}
        // TODO
        initialErrors={undefined}
        initialTouched={undefined}
        validate={undefined}
      >
        <Form>
          <SelectPaymentMethod
            label={
              <h3 className="checkout__title">
                <FormattedMessage
                  description="Checkout: select payment method"
                  defaultMessage="Select your payment method"
                />
              </h3>
            }
          />

          <h3 className="checkout__title">
            <FormattedMessage
              description="Checkout: Cart overview"
              defaultMessage="Cart overview"
            />
          </h3>

          <BodyCart store={cartStore} />
          <ErrorList errors={errors?.cart} />

          <div className="submit-wrapper">
            <button
              type="submit"
              className="btn bg-main-orange"
              disabled={!hasProducts}
            >
              <FormattedMessage
                description="Checkout: confirm order"
                defaultMessage="Place order"
              />
            </button>
          </div>
        </Form>
      </Formik>

      {/* server side submit */}
      <form ref={submitFormRef} action={confirmPath} method="post">
        <input
          type="hidden"
          name="csrfmiddlewaretoken"
          defaultValue={csrftoken}
        />
        <input type="hidden" name="checkoutData" value="" />
      </form>
    </>
  );
};

export default Payment;
