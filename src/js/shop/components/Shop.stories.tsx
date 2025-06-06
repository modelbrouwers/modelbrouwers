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
  addProductNode: HTMLFormElement | null;
  checkoutNode: HTMLDivElement | null;
}

const PRODUCTS = [
  {
    id: 1,
    name: 'Product 1',
    image: 'https://loremflickr.com/400/300/cat',
    price: 3.78,
    stock: 5,
    model_name: 'MB001',
  },
  {
    id: 2,
    name: 'Product 2',
    image: 'https://loremflickr.com/400/300/cat',
    price: 2.07,
    stock: 100,
    model_name: 'MB002',
  },
  {
    id: 888,
    name: 'Product 888',
    image: 'https://loremflickr.com/400/300/cat',
    price: 9.99,
    stock: 5,
    model_name: 'MB888',
  },
  {
    id: 999,
    name: 'Product 999',
    image: 'https://loremflickr.com/400/300/cat',
    price: 5.0,
    stock: 0,
    model_name: 'MB999',
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
  const reactCartRef = useRef<HTMLDivElement>(null);
  const reactCartDetailRef = useRef<HTMLDivElement>(null);
  const productsRef = useRef<HTMLDivElement>(null);
  const orderFormRef = useRef<HTMLFormElement>(null);
  const checkoutRef = useRef<HTMLDivElement>(null);

  const [nodes, setNodes] = useState<NodesType>({
    topbarCartNode: null,
    cartDetailNode: null,
    productsOnPage: [],
    addProductNode: null,
    checkoutNode: null,
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
      addProductNode: orderFormRef.current,
      checkoutNode: checkoutRef.current,
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

      <hr style={{borderBottom: 'solid 1px #DDD', inlineSize: '80%'}} />

      <div className="card-grid" ref={productsRef}>
        {PRODUCTS.map(({id, name, stock}) => (
          <div key={id} className="card-grid__card product-card" data-id={id} data-stock={stock}>
            <div className="product-card__name">{name}</div>
            <div className="react-cart-actions" />
          </div>
        ))}
      </div>

      <hr style={{borderBottom: 'solid 1px #DDD', inlineSize: '80%'}} />

      <article className="product">
        <h1 className="heading heading--plain">Product 888</h1>
        <form className="order-button" ref={orderFormRef}>
          <label htmlFor="amount" className="order-button__amount-label">
            Amount
          </label>
          <input type="hidden" name="productId" defaultValue="888" />
          <input
            id="amount"
            className="order-button__amount"
            type="number"
            name="amount"
            min="0"
            defaultValue="1"
          />
          <button type="submit" className="button button--blue button--order">
            Add to cart
          </button>
        </form>
      </article>

      <hr style={{borderBottom: 'solid 1px #DDD', inlineSize: '80%'}} />

      <div ref={reactCartDetailRef} id="react-cart-detail" />

      <hr style={{borderBottom: 'solid 1px #DDD', inlineSize: '80%'}} />

      <div ref={checkoutRef} id="react-checkout" />
    </div>
  );
};

export default {
  title: 'Shop / Full functionality',
  component: Shop,
  args: {
    cartDetailPath: '/winkel/cart/42/',
    checkoutPath: '/winkel/checkout/',
    indexPath: '/winkel/',
    onAddToCart: fn((productId: number, amount: number = 1): Promise<CartProductData> => {
      const newCartProduct: CartProductData = {
        id: productId,
        product: PRODUCTS.find(p => p.id === productId)!,
        amount: amount,
      };
      MOCK_CART_DATA.products.push(newCartProduct);
      return Promise.resolve({
        ...newCartProduct,
        cart: MOCK_CART_DATA.id,
      });
    }),
    onChangeAmount: fn(
      (cartProductId: number, newAmount: number): Promise<CartProductData | null> => {
        const cp = MOCK_CART_DATA.products.find(cp => cp.id === cartProductId)!;
        return Promise.resolve(
          newAmount > 0
            ? {
                id: cp.id,
                cart: MOCK_CART_DATA.id,
                product: PRODUCTS.find(p => p.id === cp.product.id)!,
                amount: newAmount,
              }
            : null,
        );
      },
    ),
    user: null, // anonymous user
    confirmPath: '/winkel/checkout/confirm/',
    checkoutUseMemoryRouter: true,
  },
  argTypes: {
    topbarCartNode: {table: {disable: true}},
    productsOnPage: {table: {disable: true}},
  },
  render: args => <ShopIndex {...args} />,
  parameters: {
    msw: {
      handlers: [
        http.get(`${API_ROOT}api/v1/shop/cart/`, () => HttpResponse.json(MOCK_CART_DATA)),
        http.get(`${API_ROOT}api/v1/shop/shipping-costs/`, () => {
          return HttpResponse.json({
            price: 11.9,
            weight: '320 g',
          });
        }),
        http.get(`${API_ROOT}api/v1/shop/paymentmethod/`, () => {
          return HttpResponse.json([
            {id: 1, name: 'Payment method 1', logo: '', order: 2},
            {id: 2, name: 'Payment method 2', logo: '', order: 3},
            {
              id: 3,
              name: 'iDeal',
              logo: '/assets/ideal-logo-1024.png',
              order: 1,
            },
          ]);
        }),
        http.get(`${API_ROOT}api/v1/shop/ideal_banks/`, () => {
          return HttpResponse.json([
            {id: 1, name: 'Bank 1'},
            {id: 2, name: 'Bank 2'},
            {id: 3, name: 'Bank 3'},
          ]);
        }),
      ],
    },
  },
} satisfies Meta<typeof Shop>;

type Story = StoryObj<typeof Shop>;

export const Default: Story = {};
