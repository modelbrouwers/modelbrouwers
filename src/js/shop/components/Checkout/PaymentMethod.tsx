import useAsync from "react-use/esm/useAsync";
// @ts-expect-error
import orderBy from "lodash.orderby";

import Radio from "@/components/forms/Radio";

import { PaymentConsumer } from "data/shop/payment";
import { ReactNode } from "react";
import { useFormikContext } from "formik";

// TODO: replace with plain fetch
const paymentConsumer = new PaymentConsumer();

interface PaymentMethod {
  id: number;
  name: string;
  logo: string;
  order: number;
}

export const useFetchPaymentMethods = () => {
  const {
    loading,
    error,
    value = [],
  } = useAsync(async () => {
    const methodList = await paymentConsumer.listMethods();
    return methodList;
  }, []);
  const paymentMethods: PaymentMethod[] = orderBy(value, ["order"], ["asc"]);
  return {
    loading,
    error,
    paymentMethods,
  };
};

interface FormikValues {
  paymentMethod: string;
  paymentMethodOptions: object;
}

export interface PaymentMethodProps {
  label: ReactNode;
  paymentMethods: PaymentMethod[];
}

const PaymentMethod: React.FC<PaymentMethodProps> = ({
  label,
  paymentMethods,
}) => {
  const { values } = useFormikContext<FormikValues>();
  const selectedOption = paymentMethods.find(
    (method) => method.id.toString() === values.paymentMethod,
  );
  console.log(selectedOption);
  return (
    <>
      <Radio
        name="paymentMethod"
        label={label}
        options={paymentMethods.map(({ id, name, logo }) => ({
          value: id.toString(),
          label: name,
          graphic: logo ? <img src={logo} alt={name} /> : undefined,
        }))}
      />
    </>
  );
};

export default PaymentMethod;
