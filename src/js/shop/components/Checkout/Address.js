import React, { useContext } from "react";
import PropTypes from "prop-types";
import { FormattedMessage } from "react-intl";
import { Formik, Form } from "formik";

import AddressFields from "./AddressFields";
import { CheckoutContext } from "./Context";
import PersonalDetailsFields from "./PersonalDetailsFields";
import Checkbox from "@/forms/Checkbox";

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

const getInitialTouched = (errors) => {
  const touched = {};
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

/**
 *
 * Address
 *
 */
const Address = ({
  customer,
  deliveryAddress,
  billingAddress = null,
  allowSubmit = false,
  onSubmit,
}) => {
  const { validationErrors } = useContext(CheckoutContext);

  return (
    <Formik
      initialValues={{
        customer,
        deliveryAddress,
        billingAddress,
        billingSameAsDelivery: true,
      }}
      initialErrors={{ validationErrors }}
      initialTouched={getInitialTouched(validationErrors)}
      onSubmit={(values) => {
        if (!allowSubmit) return;
        onSubmit(values);
      }}
    >
      {({ values, handleChange, setFieldValue }) => (
        <Form>
          <div className="row">
            {/* Personal details */}
            <div className="col-xs-12 col-md-6">
              <h3 className="checkout__title">
                <FormattedMessage
                  description="Checkout address: personal details"
                  defaultMessage="Personal details"
                />
              </h3>
              <PersonalDetailsFields customer={values.customer} />
            </div>
          </div>

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
                    description="Checkout address: billingAddressSame"
                    defaultMessage="My billing and delivery address are the same."
                  />
                }
                onChange={async (event) => {
                  handleChange(event);
                  // it's a checkbox, so the value toggles
                  const isSameAddress = !values.billingSameAsDelivery;
                  if (isSameAddress) {
                    setFieldValue("billingAddress", null);
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

          <div className="spacer" />
          <div>
            <small className="checkout__help-text">
              <FormattedMessage
                description="Checkout address: requiredFields"
                defaultMessage="* Required fields"
              />
            </small>
            <button
              type="submit"
              className="button button--blue pull-right"
              disabled={!allowSubmit}
            >
              <FormattedMessage
                description="Checkout address: continue"
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
export { AddressType, CustomerType };
