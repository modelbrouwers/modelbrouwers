import {FormattedMessage} from 'react-intl';

import {DecrementButton, IncrementButton} from './AmountButtons';

export interface AmountControlsProps {
  currentAmount: number;
  amountEditable?: boolean;
  onChangeAmount: (newAmount: number) => void;
  incrementDisabled?: boolean;
}

export const AmountControls: React.FC<AmountControlsProps> = ({
  currentAmount,
  amountEditable,
  onChangeAmount,
  incrementDisabled = false,
}) => (
  <div className="amount-controls">
    <DecrementButton onClick={() => onChangeAmount(currentAmount - 1)} />

    {amountEditable ? (
      <input
        type="number"
        name="amount"
        value={currentAmount}
        onChange={event => onChangeAmount(parseInt(event.target.value || currentAmount.toString()))}
        min={0}
        className="amount-controls__input"
      />
    ) : (
      <span className="amount-controls__current">{currentAmount}</span>
    )}

    <IncrementButton
      onClick={() => onChangeAmount(currentAmount + 1)}
      disabled={incrementDisabled}
    />
  </div>
);

export interface ProductControlsProps {
  currentAmount: number;
  amountEditable?: boolean;
  hasStock: boolean;
  onChangeAmount: (newAmount: number) => void;
  onAddProduct: () => void;
}

const ProductControls: React.FC<ProductControlsProps> = ({
  currentAmount,
  amountEditable = false,
  hasStock,
  onChangeAmount,
  onAddProduct,
}) =>
  currentAmount > 0 ? (
    <AmountControls
      currentAmount={currentAmount}
      amountEditable={amountEditable}
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
