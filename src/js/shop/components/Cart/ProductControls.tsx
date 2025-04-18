import {FormattedMessage} from 'react-intl';

import {DecrementButton, IncrementButton} from './AmountButtons';

export interface ProductControlsProps {
  currentAmount: number;
  onChangeAmount: (amount: 1 | -1) => void;
  canIncrement: boolean;
  canAdd: boolean;
  onAddProduct: () => void;
}

const ProductControls: React.FC<ProductControlsProps> = ({
  currentAmount,
  onChangeAmount,
  canIncrement,
  canAdd,
  onAddProduct,
}) => {
  if (currentAmount > 0) {
    return (
      <div className="controls__row">
        <DecrementButton onClick={() => onChangeAmount(-1)} />
        <span className="controls__amount">{currentAmount}</span>
        <IncrementButton onClick={() => onChangeAmount(-1)} disabled={!canIncrement} />
      </div>
    );
  }

  return (
    <button
      className="button button--blue button__add"
      onClick={() => onAddProduct()}
      disabled={!canAdd}
    >
      <FormattedMessage id="shop.cart.product.actions.add" defaultMessage="Add to cart" />
    </button>
  );
};

export default ProductControls;
