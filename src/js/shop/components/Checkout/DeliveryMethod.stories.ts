import type { Meta, StoryObj } from "@storybook/react";
import { withFormik } from "@/storybook/decorators";

import DeliveryMethod from "./DeliveryMethod";
import type { FormikValues } from "./Address";

export default {
  title: "Shop / Checkout / Delivery / DeliveryMethod",
  component: DeliveryMethod,
  decorators: [withFormik],
  args: {},
  parameters: {
    formik: {
      initialValues: {
        customer: {
          firstName: "",
          lastName: "",
          email: "",
          phone: "",
        },
        deliveryMethod: "mail",
        deliveryAddress: {
          company: "",
          chamberOfCommerce: "",
          street: "",
          number: "",
          city: "",
          postalCode: "",
          country: "N",
        },
        billingSameAsDelivery: true,
        billingAddress: null,
      } satisfies FormikValues,
      initialErrors: {},
    },
  },
} satisfies Meta<typeof DeliveryMethod>;

type Story = StoryObj<typeof DeliveryMethod>;

export const Default: Story = { name: "DeliveryMethod" };
