import { FormattedMessage } from "react-intl";

import Select from "@/components/forms/Select";

export interface BankOption {
  value: number; // the ID
  name: string;
}

export interface BankFieldProps {
  banks: BankOption[];
  isLoading: boolean;
}

const BankField: React.FC<BankFieldProps> = ({ banks, isLoading }) => (
  <Select<BankOption>
    name="paymentMethodOptions.bank"
    label={
      <FormattedMessage
        description="iDeal bank dropdown"
        defaultMessage="Select your bank"
      />
    }
    isLoading={isLoading}
    options={banks}
    getOptionLabel={(option) => option.name}
    required
  />
);

export default BankField;
