import {Form, Formik, FormikConfig} from 'formik';
import {useRef} from 'react';
import {FormattedMessage} from 'react-intl';

import ErrorBoundary from '@/components/ErrorBoundary.js';
import {getCsrfTokenValue} from '@/data/api-client';
import {PaymentCartOverview} from '@/shop/components/Cart';

import {useCheckoutContext} from './Context';
import {ErrorList} from './FormFields';
import SelectPaymentMethod from './SelectPaymentMethod';
import type {Address, AddressData, ConfirmOrderData} from './types';

const addressToSerializerShape = (address: Address | null): AddressData | null => {
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

const Payment: React.FC = () => {
  const {
    cartId,
    cartProducts,
    onChangeProductAmount,
    confirmPath,
    deliveryDetails,
    validationErrors,
  } = useCheckoutContext();

  const submitFormRef = useRef<HTMLFormElement>(null);

  const onFormikSubmit: FormikConfig<FormikValues>['onSubmit'] = ({
    paymentMethod,
    paymentMethodOptions,
  }) => {
    const checkoutData: ConfirmOrderData = {
      cart: cartId,
      payment_method: parseInt(paymentMethod, 10),
      payment_method_options: paymentMethodOptions,
      first_name: deliveryDetails.customer.firstName,
      last_name: deliveryDetails.customer.lastName,
      email: deliveryDetails.customer.email,
      phone: deliveryDetails.customer.phone,
      delivery_method: deliveryDetails.deliveryMethod,
      delivery_address: addressToSerializerShape(deliveryDetails.deliveryAddress),
      invoice_address: addressToSerializerShape(deliveryDetails.billingAddress),
    };

    const form = submitFormRef.current;
    if (form === null) throw new Error('form ref should not be null');
    const checkoutDataInput = form.querySelector<HTMLInputElement>('input[name="checkoutData"]');
    checkoutDataInput!.value = JSON.stringify(checkoutData);
    form.submit();
  };

  const hasProducts = Boolean(cartProducts.length);
  return (
    <>
      <Formik<FormikValues>
        initialValues={{
          paymentMethod: '',
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
          <ErrorBoundary>
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
          </ErrorBoundary>

          <h3 className="checkout__title">
            <FormattedMessage
              description="Checkout: Cart overview"
              defaultMessage="Cart overview"
            />
          </h3>

          <PaymentCartOverview cartProducts={cartProducts} onChangeAmount={onChangeProductAmount} />
          {/* @ts-expect-error */}
          <ErrorList errors={validationErrors?.cart} />

          <div className="submit-wrapper">
            <button type="submit" className="btn bg-main-orange" disabled={!hasProducts}>
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
        <input type="hidden" name="csrfmiddlewaretoken" defaultValue={getCsrfTokenValue()} />
        <input type="hidden" name="checkoutData" value="" />
      </form>
    </>
  );
};

export default Payment;
