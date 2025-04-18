import type {Meta, StoryObj} from '@storybook/react';
import {useEffect, useRef, useState} from 'react';

import Shop from './Shop';

interface NodesType {
  topbarCartNode: HTMLDivElement | null;
  cartDetailNode: HTMLDivElement | null;
}

export default {
  title: 'Shop / Full functionality',
  component: Shop,
  args: {
    cartDetailPath: '/winkel/cart/42/',
    checkoutPath: '/winkel/checkout/',
  },
  render: args => {
    const reactCartRef = useRef<HTMLDivElement | null>(null);
    const reactCartDetailRef = useRef<HTMLDivElement | null>(null);
    const [nodes, setNodes] = useState<NodesType>({topbarCartNode: null, cartDetailNode: null});

    useEffect(() => {
      setNodes({
        topbarCartNode: reactCartRef.current,
        cartDetailNode: reactCartDetailRef.current,
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
        }}
      >
        <div ref={reactCartRef} id="react-cart" />
        <div ref={reactCartDetailRef} id="react-cart-detail" />
        <Shop {...args} {...nodes} />
      </div>
    );
  },
} satisfies Meta<typeof Shop>;

type Story = StoryObj<typeof Shop>;

export const Default: Story = {};
