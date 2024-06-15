import React, { useContext, useState } from "react";
import PropTypes from "prop-types";
import { FormattedMessage } from "react-intl";
import { useNavigate } from "react-router-dom";
import { Formik, Form } from "formik";

import AddressFields from "./AddressFields";
import { SUPPORTED_COUNTRIES, EMPTY_ADDRESS } from "./constants";
import { CheckoutContext } from "./Context";
import PersonalDetailsFields from "./PersonalDetailsFields";

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
  billingAddress,
  allowSubmit = false,
  onChange,
  onSubmit,
}) => {
  const [deliveryAddressIsBillingAddress, setDeliveryAddressIsBillingAddress] =
    useState(true);
  const navigate = useNavigate();
  const { validationErrors } = useContext(CheckoutContext);

  billingAddress =
    billingAddress ?? (!deliveryAddressIsBillingAddress ? EMPTY_ADDRESS : null);

  return (
    <Formik
      initialValues={{
        customer,
        deliveryAddress,
        billingAddress,
      }}
      initialErrors={{ validationErrors }}
      initialTouched={getInitialTouched(validationErrors)}
      onSubmit={(values) => {
        if (!allowSubmit) return;
        onSubmit(values);
      }}
    >
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

            <PersonalDetailsFields
              prefix="customer"
              firstName={customer.firstName}
              lastName={customer.lastName}
              email={customer.email}
              phone={customer.phone}
              errors={validationErrors?.customer}
              onChange={onChange}
            />
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

            <div className="form-check checkbox-flex">
              <input
                type="checkbox"
                className="form-check-input"
                id="deliveryAddressIsBillingAddress"
                checked={deliveryAddressIsBillingAddress}
                onChange={() => {
                  setDeliveryAddressIsBillingAddress(
                    !deliveryAddressIsBillingAddress,
                  );
                  onChange({
                    target: {
                      name: "billingAddress",
                      value: null,
                    },
                  });
                }}
              />
              <label
                className="form-check-label"
                htmlFor="deliveryAddressIsBillingAddress"
              >
                <FormattedMessage
                  description="Checkout address: billingAddressSame"
                  defaultMessage="My billing and delivery address are the same."
                />
              </label>
            </div>
          </div>

          {/*Billing address*/}
          {!deliveryAddressIsBillingAddress && (
            <div className="col-md-6 col-xs-12">
              <h3 className="checkout__title">
                <FormattedMessage
                  description="Billing address: billingAddress"
                  defaultMessage="Billing address"
                />
              </h3>

              {/* TODO: fix default country being reset */}
              <AddressFields prefix="billingAddress" />
            </div>
          )}
        </div>

        <div className="spacer" />
        <div>
          <small className="checkout__help-text">
            *{" "}
            <FormattedMessage
              description="Checkout address: requiredFields"
              defaultMessage="Required fields"
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
    </Formik>
  );
};

Address.propTypes = {
  customer: CustomerType,
  deliveryAddress: AddressType.isRequired,
  billingAddress: AddressType,
  onChange: PropTypes.func.isRequired,
  allowSubmit: PropTypes.bool,
};

export default Address;
export { AddressType, CustomerType };
