import {DEFAULT_IMAGE} from '@/constants.js';
import type {Product} from '@/data/shop/cart';

export interface ProductImageProps extends React.ComponentProps<'img'> {
  product: Product;
}

const ProductImage: React.FC<ProductImageProps> = ({product, ...props}) => (
  <img
    src={product.image || DEFAULT_IMAGE}
    alt={product.name}
    onError={event => {
      event.currentTarget.onerror = null;
      event.currentTarget.src = DEFAULT_IMAGE;
    }}
    {...props}
  />
);

export default ProductImage;
