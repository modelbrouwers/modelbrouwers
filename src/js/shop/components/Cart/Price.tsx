import {FormattedNumber} from 'react-intl';

export interface PriceProps {
  value: number;
}

const Price: React.FC<PriceProps> = ({value}) => {
  return <FormattedNumber value={value} style="currency" currency="EUR" />;
};

export default Price;
