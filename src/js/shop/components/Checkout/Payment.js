import React, { useEffect, useRef, useState } from "react";
import PropTypes from "prop-types";
import classNames from "classnames";
import orderBy from "lodash.orderby";
import { FormattedMessage } from "react-intl";
import Select from "react-select";
import useAsync from "react-use/esm/useAsync";
import { Formik, Form } from "formik";

import Loader from "components/Loader";
import ErrorBoundary from "components/ErrorBoundary";
import Radio from "@/components/forms/Radio";

import { ErrorMessage } from "../Info";
import { FormField, FormGroup, ErrorList } from "./FormFields";
import { BodyCart } from "../Cart";
import SelectPaymentMethod from "./SelectPaymentMethod";

const AddressType = PropTypes.shape({
  company: PropTypes.string,
  chamberOfCommerce: PropTypes.string,
  street: PropTypes.string,
  number: PropTypes.string,
  city: PropTypes.string,
  postalCode: PropTypes.string,
  country: PropTypes.string,
});

const CustomerType = PropTypes.shape({
  firstName: PropTypes.string,
  lastName: PropTypes.string,
  email: PropTypes.string,
  phone: PropTypes.string,
});

const addressToSerializerShape = (address) => {
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

/**
 *
 * Payment method selection & flow
 *
 */
const Payment = ({
  cartStore,
  csrftoken,
  confirmPath,
  errors,
  checkoutDetails,
}) => {
  const submitFormRef = useRef();

  const onFormikSubmit = ({ paymentMethod, paymentMethodOptions }) => {
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
    const checkoutDataInput = form.querySelector('input[name="checkoutData"]');
    checkoutDataInput.value = JSON.stringify(checkoutData);
    form.submit();
  };

  const hasProducts = Boolean(cartStore.products.length);
  return (
    <>
      <Formik
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

Payment.propTypes = {
  cartStore: PropTypes.object.isRequired,
  csrftoken: PropTypes.string.isRequired,
  confirmPath: PropTypes.string.isRequired,
  errors: PropTypes.object,
  checkoutDetails: PropTypes.shape({
    customer: CustomerType.isRequired,
    deliveryAddress: AddressType.isRequired,
    billingAddress: AddressType,
  }).isRequired,
};

export default Payment;
