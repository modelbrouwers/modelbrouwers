import {useFormikContext} from 'formik';
import orderBy from 'lodash/orderBy';
import {ReactNode, useEffect} from 'react';
import useAsync from 'react-use/esm/useAsync';

import ErrorBoundary from 'components/ErrorBoundary.js';
import {PaymentConsumer} from 'data/shop/payment';

import Loader from '@/components/Loader';
import Radio from '@/components/forms/Radio';

import {ErrorMessage} from '../Info';
import BankField from './BankField';

// TODO: replace with plain fetch
const paymentConsumer = new PaymentConsumer();

// AVAILABLE PAYMENT METHODS

interface PaymentMethod {
  id: number;
  name: string;
  logo: string;
  order: number;
}

const useFetchPaymentMethods = () => {
  const {
    loading,
    error,
    value = [],
  } = useAsync(async () => {
    const methodList = await paymentConsumer.listMethods();
    return methodList;
  }, []);
  const paymentMethods: PaymentMethod[] = orderBy(value, ['order'], ['asc']);
  return {
    loading,
    error,
    paymentMethods,
  };
};

// IDEAL BANKS
interface IDealBank {
  id: number;
  name: string;
}

const useFetchIDealBanks = () => {
  const {
    loading,
    error,
    value = [],
  } = useAsync(async () => {
    const response: {responseData: IDealBank[]} = await paymentConsumer.listIdealBanks();
    return response.responseData;
  }, []);
  return {loading, error, banks: value};
};

// FULL PAYMENT METHOD SELECTION

interface FormikValues {
  paymentMethod: string;
  paymentMethodOptions: object;
}

export interface SelectPaymentMethodProps {
  label: ReactNode;
}

const SelectPaymentMethod: React.FC<SelectPaymentMethodProps> = ({label}) => {
  const {loading, error, paymentMethods = []} = useFetchPaymentMethods();

  // pre-load the ideal banks
  const {loading: loadingBanks, error: banksError, banks} = useFetchIDealBanks();
  if (banksError) throw banksError;

  const {
    values: {paymentMethod},
    setFieldValue,
  } = useFormikContext<FormikValues>();
  const selectedOption = paymentMethods.find(method => method.id.toString() === paymentMethod);

  // whenever the payment method changes, reset the paymentMethodOptions
  useEffect(() => {
    setFieldValue('paymentMethodOptions', {});
  }, [paymentMethod]);

  if (error) return <ErrorMessage />;

  return (
    <>
      {loading ? (
        <Loader center />
      ) : (
        <Radio
          name="paymentMethod"
          label={label}
          options={paymentMethods.map(({id, name, logo}) => ({
            value: id.toString(),
            label: name,
            graphic: logo ? <img src={logo} alt={name} /> : undefined,
          }))}
        />
      )}

      <ErrorBoundary>
        {selectedOption?.name.toLowerCase() === 'ideal' && (
          <BankField
            isLoading={loadingBanks}
            banks={banks.map(({id, name}) => ({value: id, name}))}
          />
        )}
      </ErrorBoundary>
    </>
  );
};

export default SelectPaymentMethod;
