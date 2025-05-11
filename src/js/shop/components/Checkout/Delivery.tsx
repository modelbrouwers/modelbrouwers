import {Form, Formik, FormikErrors} from 'formik';
import {FormattedMessage, useIntl} from 'react-intl';
import {useNavigate} from 'react-router';

import Checkbox from '@/components/forms/Checkbox';

import AddressFields from './AddressFields';
import {useCheckoutContext} from './Context';
import DeliveryMethod from './DeliveryMethod';
import PersonalDetailsFields from './PersonalDetailsFields';
import ShippingCosts from './ShippingCosts';
import type {DeliveryDetails} from './types';
import {validateAddressDetails} from './validation';

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
      case 'string': {
        touched[key] = true;
        break;
      }
      case 'object': {
        touched[key] = getInitialTouched(errorOrObject);
        break;
      }
    }
  });
  return touched;
};

const Delivery: React.FC = () => {
  const intl = useIntl();
  const navigate = useNavigate();
  const {
    deliveryDetails,
    setDeliveryDetails,
    validationErrors: _validationErrors,
  } = useCheckoutContext();
  // FIXME -> in context type
  const validationErrors = _validationErrors as FormikErrors<FormikValues>;
  return (
    <Formik<FormikValues>
      initialValues={{
        ...deliveryDetails,
        billingSameAsDelivery: deliveryDetails.billingAddress == null,
      }}
      enableReinitialize
      initialErrors={validationErrors}
      initialTouched={getInitialTouched(validationErrors)}
      onSubmit={async values => {
        setDeliveryDetails(values);
        navigate('/payment');
      }}
      validate={values => validateAddressDetails(values, intl)}
      validateOnMount
    >
      {({values, handleChange, setFieldValue, isValid, isValidating, setFieldTouched}) => (
        <Form style={{display: 'flex', flexDirection: 'column', gap: '15px'}}>
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
                <ShippingCosts />
              </div>
            </div>
          </div>

          {values.deliveryMethod === 'mail' && (
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
                  onChange={async event => {
                    handleChange(event);
                    // it's a checkbox, so the value toggles
                    const isSameAddress = !values.billingSameAsDelivery;
                    if (isSameAddress) {
                      setFieldValue('billingAddress', null);
                      setFieldTouched('billingAddress', undefined);
                    } else {
                      const emptyAddress = {
                        company: '',
                        chamberOfCommerce: '',
                        street: '',
                        number: '',
                        city: '',
                        postalCode: '',
                        country: values.deliveryAddress.country || 'N',
                      };
                      setFieldValue('billingAddress', emptyAddress);
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

export default Delivery;
