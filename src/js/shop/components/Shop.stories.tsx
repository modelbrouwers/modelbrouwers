import type {Meta, StoryObj} from '@storybook/react';
import {fn} from '@storybook/test';
import {HttpResponse, http} from 'msw';
import {useEffect, useRef, useState} from 'react';

import {API_ROOT} from '@/constants.js';
import type {CartData, CartProductData} from '@/data/shop/cart';

import Shop, {type CatalogueProduct} from './Shop';

interface NodesType {
  topbarCartNode: HTMLDivElement | null;
  cartDetailNode: HTMLDivElement | null;
  productsOnPage: CatalogueProduct[];
}

const PRODUCTS = [
  {
    id: 1,
    name: 'Product 1',
    image: 'https://loremflickr.com/400/300/cat',
    price: 3.78,
    stock: 5,
  },
  {
    id: 2,
    name: 'Product 2',
    image: 'https://loremflickr.com/400/300/cat',
    price: 2.07,
    stock: 100,
  },
  {
    id: 888,
    name: 'Product 888',
    image: 'https://loremflickr.com/400/300/cat',
    price: 9.99,
    stock: 5,
  },
  {
    id: 999,
    name: 'Product 999',
    image: 'https://loremflickr.com/400/300/cat',
    price: 5.0,
    stock: 0,
  },
];

const MOCK_CART_DATA: CartData = {
  id: 42,
  user: null,
  products: [
    {
      id: 1,
      product: PRODUCTS.find(p => p.id === 1)!,
      amount: 1,
    },
    {
      id: 2,
      product: PRODUCTS.find(p => p.id === 2)!,
      amount: 3,
    },
  ],
};

const ShopIndex: React.FC<React.ComponentProps<typeof Shop>> = ({...args}) => {
  const reactCartRef = useRef<HTMLDivElement | null>(null);
  const reactCartDetailRef = useRef<HTMLDivElement | null>(null);
  const productsRef = useRef<HTMLDivElement | null>(null);

  const [nodes, setNodes] = useState<NodesType>({
    topbarCartNode: null,
    cartDetailNode: null,
    productsOnPage: [],
  });

  useEffect(() => {
    const cardNodes = productsRef.current!.querySelectorAll<HTMLDivElement>('.product-card');
    const productsOnPage = Array.from(cardNodes).map((node): CatalogueProduct => {
      const {id = '0', stock = '0'} = node.dataset;
      const controlsNode = node.querySelector<HTMLDivElement>('.react-cart-actions');
      return {id: parseInt(id), stock: parseInt(stock), controlsNode: controlsNode!};
    });
    setNodes({
      topbarCartNode: reactCartRef.current,
      cartDetailNode: reactCartDetailRef.current,
      productsOnPage: productsOnPage,
    });
  }, []);

  return (
    <div
      style={{
        maxInlineSize: '800px',
        boxShadow: '1px 1px 5px 0px rgba(0, 0, 0, 0.2)',
        border: 'solid 1px rgba(0, 0, 0, 0.2)',
        padding: '15px',
        marginInlineEnd: 'auto',
        marginInlineStart: 'auto',
        display: 'flex',
        flexDirection: 'column',
        rowGap: '15px',
      }}
    >
      <Shop {...args} {...nodes} />
      <div ref={reactCartRef} id="react-cart" />
      <div ref={reactCartDetailRef} id="react-cart-detail" />

      <div className="card-grid" ref={productsRef}>
        {PRODUCTS.map(({id, name, stock}) => (
          <div key={id} className="card-grid__card product-card" data-id={id} data-stock={stock}>
            <div className="product-card__name">{name}</div>
            <div className="react-cart-actions" />
          </div>
        ))}
      </div>
    </div>
  );
};

export default {
  title: 'Shop / Full functionality',
  component: Shop,
  args: {
    cartDetailPath: '/winkel/cart/42/',
    checkoutPath: '/winkel/checkout/',
    onAddToCart: fn(
      (productId: number): Promise<CartProductData> =>
        Promise.resolve({
          id: productId,
          product: PRODUCTS.find(p => p.id === productId)!,
          amount: 1,
        }),
    ),
    onChangeAmount: fn(),
  },
  render: args => <ShopIndex {...args} />,
  parameters: {
    msw: {
      handlers: [http.get(`${API_ROOT}api/v1/shop/cart/`, () => HttpResponse.json(MOCK_CART_DATA))],
    },
  },
} satisfies Meta<typeof Shop>;

type Story = StoryObj<typeof Shop>;

export const Default: Story = {};
