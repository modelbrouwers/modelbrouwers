import {FormattedMessage} from 'react-intl';

import {DecrementButton, IncrementButton} from './AmountButtons';

export interface AmountControlsProps {
  currentAmount: number;
  onChangeAmount: (newAmount: number) => void;
  incrementDisabled?: boolean;
}

export const AmountControls: React.FC<AmountControlsProps> = ({
  currentAmount,
  onChangeAmount,
  incrementDisabled = false,
}) => (
  <div className="controls__row">
    <DecrementButton onClick={() => onChangeAmount(currentAmount - 1)} />
    <span className="controls__amount">{currentAmount}</span>
    <IncrementButton
      onClick={() => onChangeAmount(currentAmount + 1)}
      disabled={incrementDisabled}
    />
  </div>
);

export interface ProductControlsProps {
  currentAmount: number;
  hasStock: boolean;
  onChangeAmount: (newAmount: number) => void;
  onAddProduct: () => void;
}

const ProductControls: React.FC<ProductControlsProps> = ({
  currentAmount,
  hasStock,
  onChangeAmount,
  onAddProduct,
}) =>
  currentAmount > 0 ? (
    <AmountControls
      currentAmount={currentAmount}
      onChangeAmount={onChangeAmount}
      incrementDisabled={!hasStock}
    />
  ) : (
    <button
      className="button button--blue button__add"
      onClick={() => onAddProduct()}
      disabled={!hasStock}
    >
      <FormattedMessage id="shop.cart.product.actions.add" defaultMessage="Add to cart" />
    </button>
  );

export default ProductControls;
