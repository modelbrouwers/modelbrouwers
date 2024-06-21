import type { Meta, StoryObj } from "@storybook/react";
import { withFormik } from "@/storybook/decorators";

import DeliveryMethod from "./DeliveryMethod";

export default {
  title: "Shop / Checkout / Delivery / DeliveryMethod",
  component: DeliveryMethod,
  decorators: [withFormik],
  args: {},
  parameters: {
    formik: {
      initialValues: {
        deliveryMethod: null,
      },
      initialErrors: {},
    },
  },
} satisfies Meta<typeof DeliveryMethod>;

type Story = StoryObj<typeof DeliveryMethod>;

export const Default: Story = { name: "DeliveryMethod" };
