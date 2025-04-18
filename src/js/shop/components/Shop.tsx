import {createPortal} from 'react-dom';

export interface ShopProps {
  topbarCartNode: HTMLDivElement | null;
}

/**
 * Main component to manage everything web shop related.
 *
 * Takes care of tracking the shop state and renders all sub components into their
 * assigned portal nodes.
 */
const Shop: React.FC<ShopProps> = ({topbarCartNode}) => {
  console.log(topbarCartNode);
  if (!topbarCartNode) return null;

  return createPortal(<p>Henlo</p>, topbarCartNode);
};

export default Shop;
