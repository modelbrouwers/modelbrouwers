import {FormattedMessage} from 'react-intl';

import {DecrementButton, IncrementButton} from './AmountButtons';

export interface ProductControlsProps {
  currentAmount: number;
  hasStock: boolean;
  onChangeAmount: (amount: 1 | -1) => void;
  onAddProduct: () => void;
}

const ProductControls: React.FC<ProductControlsProps> = ({
  currentAmount,
  hasStock,
  onChangeAmount,
  onAddProduct,
}) => {
  if (currentAmount > 0) {
    return (
      <div className="controls__row">
        <DecrementButton onClick={() => onChangeAmount(-1)} />
        <span className="controls__amount">{currentAmount}</span>
        <IncrementButton onClick={() => onChangeAmount(1)} disabled={!hasStock} />
      </div>
    );
  }

  return (
    <button
      className="button button--blue button__add"
      onClick={() => onAddProduct()}
      disabled={!hasStock}
    >
      <FormattedMessage id="shop.cart.product.actions.add" defaultMessage="Add to cart" />
    </button>
  );
};

export default ProductControls;
