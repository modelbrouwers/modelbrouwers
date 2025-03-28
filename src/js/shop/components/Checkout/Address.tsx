import { useContext } from "react";
import { FormattedMessage, useIntl } from "react-intl";
import { Formik, Form, FormikErrors } from "formik";

import Checkbox from "@/components/forms/Checkbox";
import type { CartStore } from "@/shop/store";
import ErrorBoundary from "@/components/ErrorBoundary.js";

import AddressFields from "./AddressFields";
import { CheckoutContext } from "./Context";
import DeliveryMethod from "./DeliveryMethod";
import PersonalDetailsFields from "./PersonalDetailsFields";
import ShippingCosts from "./ShippingCosts";
import type { Address as AddressType, DeliveryDetails } from "./types";
import { validateAddressDetails } from "./validation";

export const EMPTY_ADDRESS: AddressType = {
  company: "",
  chamberOfCommerce: "",
  street: "",
  number: "",
  city: "",
  postalCode: "",
  country: "N",
};

export type AddressProps = DeliveryDetails & {
  cartStore: CartStore;
  onSubmit: (values: DeliveryDetails) => void;
};

export type FormikValues = DeliveryDetails & {
  billingSameAsDelivery: boolean;
};

// FIXME: could probably be done in a type safe way, but it is complicated so maybe it's
// just a bad idea?
type Touched = {
  [K in string]: any;
};

const getInitialTouched = (errors: any) => {
  const touched: Touched = {};
  if (!errors) return touched;

  Object.entries(errors).forEach(([key, errorOrObject]) => {
    switch (typeof errorOrObject) {
      case "string": {
        touched[key] = true;
        break;
      }
      case "object": {
        touched[key] = getInitialTouched(errorOrObject);
        break;
      }
    }
  });
  return touched;
};

const Address: React.FC<AddressProps> = ({
  cartStore,
  customer,
  deliveryAddress,
  billingAddress,
  onSubmit,
}) => {
  const intl = useIntl();
  const { validationErrors: _validationErrors } = useContext(CheckoutContext);
  // FIXME -> in context type
  const validationErrors = _validationErrors as FormikErrors<FormikValues>;
  return (
    <Formik<FormikValues>
      initialValues={{
        customer,
        deliveryMethod: "mail",
        deliveryAddress: deliveryAddress || EMPTY_ADDRESS,
        billingAddress,
        billingSameAsDelivery: billingAddress == null,
      }}
      enableReinitialize
      initialErrors={validationErrors}
      initialTouched={getInitialTouched(validationErrors)}
      onSubmit={onSubmit}
      validate={(values) => validateAddressDetails(values, intl)}
      validateOnMount
    >
      {({
        values,
        handleChange,
        setFieldValue,
        isValid,
        isValidating,
        setFieldTouched,
      }) => (
        <Form style={{ display: "flex", flexDirection: "column", gap: "15px" }}>
          <div className="row">
            {/* Personal details */}
            <div className="col-xs-12 col-md-6">
              <h3 className="checkout__title">
                <FormattedMessage
                  description="Delivery details: personal details"
                  defaultMessage="Personal details"
                />
              </h3>
              <PersonalDetailsFields customer={values.customer} />
            </div>
          </div>

          <div className="row">
            {/* Delivery method */}
            <div className="col-xs-12 col-md-6">
              <h3 className="checkout__title">
                <FormattedMessage
                  description="Delivery details: delivery method"
                  defaultMessage="Delivery or pickup?"
                />
              </h3>
              <DeliveryMethod />
              <div aria-live="polite">
                <ErrorBoundary>
                  <ShippingCosts cartStore={cartStore} />
                </ErrorBoundary>
              </div>
            </div>
          </div>

          {values.deliveryMethod === "mail" && (
            <div className="row">
              {/* Delivery address */}
              <div className="col-md-6 col-xs-12">
                <h3 className="checkout__title">
                  <FormattedMessage
                    description="Delivery address: deliveryAddress"
                    defaultMessage="Delivery address"
                  />
                </h3>

                <AddressFields prefix="deliveryAddress" />

                <Checkbox
                  name="billingSameAsDelivery"
                  label={
                    <FormattedMessage
                      description="Delivery details: billingAddressSame"
                      defaultMessage="My billing and delivery address are the same."
                    />
                  }
                  onChange={async (event) => {
                    handleChange(event);
                    // it's a checkbox, so the value toggles
                    const isSameAddress = !values.billingSameAsDelivery;
                    if (isSameAddress) {
                      setFieldValue("billingAddress", null);
                      setFieldTouched("billingAddress", undefined);
                    } else {
                      const emptyAddress = {
                        company: "",
                        chamberOfCommerce: "",
                        street: "",
                        number: "",
                        city: "",
                        postalCode: "",
                        country: values.deliveryAddress.country || "N",
                      };
                      setFieldValue("billingAddress", emptyAddress);
                    }
                  }}
                />
              </div>

              {/*Billing address*/}
              {!values.billingSameAsDelivery && (
                <div className="col-md-6 col-xs-12">
                  <h3 className="checkout__title">
                    <FormattedMessage
                      description="Billing address: billingAddress"
                      defaultMessage="Billing address"
                    />
                  </h3>
                  <AddressFields prefix="billingAddress" />
                </div>
              )}
            </div>
          )}

          <div className="spacer" />
          <div>
            <small className="checkout__help-text">
              <FormattedMessage
                description="Delivery details: requiredFields"
                defaultMessage="* Required fields"
              />
            </small>
            <button
              type="submit"
              className="button button--blue pull-right"
              disabled={isValidating || !isValid}
            >
              <FormattedMessage
                description="Delivery details: continue"
                defaultMessage="Continue"
              />
            </button>
          </div>
        </Form>
      )}
    </Formik>
  );
};

export default Address;
