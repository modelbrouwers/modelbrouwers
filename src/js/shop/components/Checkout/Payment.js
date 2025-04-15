import classNames from 'classnames';
import orderBy from 'lodash/orderBy';
import PropTypes from 'prop-types';
import React, {useEffect, useState} from 'react';
import {FormattedMessage} from 'react-intl';
import Select from 'react-select';
import useAsync from 'react-use/esm/useAsync';

import ErrorBoundary from 'components/ErrorBoundary';
import Loader from 'components/Loader';

import {PaymentConsumer} from '../../../data/shop/payment';
import {BodyCart} from '../Cart';
import {ErrorMessage} from '../Info';
import {ErrorList, FormField, FormGroup} from './FormFields';

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

const paymentConsumer = new PaymentConsumer();

const useFetchPaymentMethods = () => {
  const {
    loading,
    error,
    value = [],
  } = useAsync(async () => {
    const methodList = await paymentConsumer.listMethods();
    return methodList;
  }, []);
  const paymentMethods = orderBy(value, ['order'], ['asc']);
  return {
    loading,
    error,
    paymentMethods,
  };
};

const PaymentMethod = ({id, name, order, logo = null, isSelected = false, onChange}) => {
  const className = classNames('payment-method', {
    'payment-method--has-logo': !!logo,
    'payment-method--active': isSelected,
  });

  return (
    <label className={className}>
      <input
        type="radio"
        className="payment-methods__input"
        id={`paymentmethod-${id}`}
        name="paymentMethod"
        value={id}
        onChange={onChange}
        checked={isSelected}
      />
      <div className="payment-method__logo">{logo && <img src={logo} alt={name} />}</div>
      <span className="payment-method__name">{name}</span>
    </label>
  );
};

PaymentMethod.propTypes = {
  id: PropTypes.number.isRequired,
  name: PropTypes.string.isRequired,
  order: PropTypes.number.isRequired,
  logo: PropTypes.string,
  isSelected: PropTypes.bool,
  onChange: PropTypes.func.isRequired,
};

const useGetPaymentSpecificOptions = paymentMethod => {
  const {
    loading,
    error,
    value = {},
  } = useAsync(async () => {
    if (!paymentMethod) return;

    switch (paymentMethod.name.toLowerCase()) {
      case 'ideal': {
        const idealBanks = await paymentConsumer.listIdealBanks();
        return {banks: idealBanks.responseData};
      }
    }
  }, [paymentMethod]);

  // TODO: properly set up user feedback with error boundaries
  if (error) {
    throw error;
  }

  return value;
};

const PaymentMethodSpecificOptions = ({
  paymentMethod,
  paymentMethodSpecificState,
  setPaymentMethodSpecificState,
  ...props
}) => {
  if (!paymentMethod) return null;

  switch (paymentMethod.name.toLowerCase()) {
    case 'ideal': {
      const {banks} = props;
      if (!banks) return <Loader />;

      const onBankChange = bank => {
        setPaymentMethodSpecificState({
          ...paymentMethodSpecificState,
          bank,
        });
      };

      return (
        <>
          <div className="spacer" />
          <FormGroup>
            <FormField
              name="bank"
              label={
                <FormattedMessage
                  description="iDeal bank dropdown"
                  defaultMessage="Select your bank"
                />
              }
              required
              component={Select}
              value={paymentMethodSpecificState.bank}
              options={banks.map(bank => ({
                value: bank.id,
                label: bank.name,
              }))}
              onChange={onBankChange}
              className=""
              autoFocus={!paymentMethodSpecificState.bank}
            />
          </FormGroup>
        </>
      );
    }
  }

  return null;
};

PaymentMethodSpecificOptions.propTypes = {
  paymentMethod: PropTypes.shape({
    id: PropTypes.number.isRequired,
    name: PropTypes.string.isRequired,
    order: PropTypes.number.isRequired,
    logo: PropTypes.string,
  }),
};

const addressToSerializerShape = address => {
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
const Payment = ({cartStore, csrftoken, confirmPath, errors, checkoutDetails}) => {
  const {loading, error, paymentMethods} = useFetchPaymentMethods();
  const [selectedMethod, setSelectedMethod] = useState(null);
  const [paymentMethodSpecificState, setPaymentMethodSpecificState] = useState({});
  const paymentMethod = paymentMethods.find(method => method.id === selectedMethod);
  const paymentMethodOptions = useGetPaymentSpecificOptions(paymentMethod);

  if (error) return <ErrorMessage />;

  const checkoutData = {
    cart: cartStore.id,
    payment_method: selectedMethod,
    payment_method_options: paymentMethodSpecificState,
    first_name: checkoutDetails.customer.firstName,
    last_name: checkoutDetails.customer.lastName,
    email: checkoutDetails.customer.email,
    phone: checkoutDetails.customer.phone,
    delivery_address: addressToSerializerShape(checkoutDetails.deliveryAddress),
    invoice_address: addressToSerializerShape(checkoutDetails.billingAddress),
  };

  const hasProducts = Boolean(cartStore.products.length);

  return (
    <>
      <h3 className="checkout__title">
        <FormattedMessage
          description="Checkout: select payment method"
          defaultMessage="Select your payment method"
        />
      </h3>

      {loading && <Loader />}

      <div className="payment-methods">
        {paymentMethods.map(method => (
          <PaymentMethod
            key={method.id}
            {...method}
            isSelected={paymentMethod && method.id === paymentMethod.id}
            onChange={event => setSelectedMethod(parseInt(event.target.value, 10))}
          />
        ))}
      </div>

      <ErrorBoundary>
        <PaymentMethodSpecificOptions
          paymentMethod={paymentMethod}
          paymentMethodSpecificState={paymentMethodSpecificState}
          setPaymentMethodSpecificState={setPaymentMethodSpecificState}
          {...paymentMethodOptions}
        />
      </ErrorBoundary>

      <h3 className="checkout__title">
        <FormattedMessage description="Checkout: Cart overview" defaultMessage="Cart overview" />
      </h3>

      <BodyCart store={cartStore} />
      <ErrorList errors={errors?.cart} />

      {/* server side submit */}
      <form action={confirmPath} method="post">
        <input type="hidden" name="csrfmiddlewaretoken" defaultValue={csrftoken} />
        <input type="hidden" name="checkoutData" value={JSON.stringify(checkoutData)} />
        <div className="submit-wrapper">
          <button type="submit" className="btn bg-main-orange" disabled={!hasProducts}>
            <FormattedMessage description="Checkout: confirm order" defaultMessage="Place order" />
          </button>
        </div>
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
