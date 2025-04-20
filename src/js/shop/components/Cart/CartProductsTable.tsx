import React from 'react';
import {FormattedMessage} from 'react-intl';

import {CartProduct} from '@/shop/data';

import Price from './Price';
import {AmountControls} from './ProductControls';
import ProductImage from './ProductImage';
import messages from './messages';

export type Column = keyof typeof messages;

export interface CartProductsTableHeaderProps {
  columns: Column[];
}

export const CartProductsTableHeader: React.FC<CartProductsTableHeaderProps> = ({columns}) => (
  <thead className="cart-products-table-header">
    <tr>
      {columns.map(column => (
        <th key={column} className={`cart-products-table-header__col-${column}`}>
          <FormattedMessage key={column} {...messages[column]} />
        </th>
      ))}
    </tr>
  </thead>
);

export interface CartProductRowProps {
  columns: Column[];
  cartProduct: CartProduct;
  amountEditable?: boolean;
  onChangeAmount: (cartProductId: number, newAmount: number) => Promise<void>;
}

export const CartProductRow: React.FC<CartProductRowProps> = ({
  columns,
  cartProduct,
  amountEditable,
  onChangeAmount,
}) => {
  const columnElements: Record<Column, React.ReactElement> = {
    image: (
      <td>
        <ProductImage product={cartProduct.product} className="cart-product-row__product-image" />
      </td>
    ),
    productName: (
      <td>
        <a href="#">{cartProduct.product.name}</a>
      </td>
    ),
    model: <td>{cartProduct.product.model_name}</td>,
    quantity: (
      <td className="cart-product-row__quantity">
        <AmountControls
          currentAmount={cartProduct.amount}
          amountEditable={amountEditable}
          onChangeAmount={(newAmount: number) => onChangeAmount(cartProduct.id, newAmount)}
        />
      </td>
    ),
    unitPrice: (
      <td>
        <Price value={cartProduct.product.price} />
      </td>
    ),
    totalHeader: (
      <td>
        <Price value={cartProduct.total} />
      </td>
    ),
  };

  return (
    <tr className="cart-product-row">
      {columns.map(column => (
        <React.Fragment key={column}>{columnElements[column]}</React.Fragment>
      ))}
    </tr>
  );
};
