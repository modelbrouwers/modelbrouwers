import type { Meta, StoryObj } from "@storybook/react";
import { withFormik } from "@/storybook/decorators";

import AddressFields from "./AddressFields";

export default {
  title: "Shop / Checkout / AddressFields",
  component: AddressFields,
  decorators: [withFormik],
  args: {
    prefix: "prefix",
  },
  argTypes: {
    prefix: { control: { disable: true } },
  },
  parameters: {
    formik: {
      initialValues: {
        prefix: {
          company: "",
          chamberOfCommerce: "",
          street: "",
          number: "",
          city: "",
          postalCode: "",
          country: null,
        },
      },
      initialErrors: {},
    },
  },
} satisfies Meta<typeof AddressFields>;

type Story = StoryObj<typeof AddressFields>;

export const Empty: Story = {};

export const FilledOut: Story = {
  parameters: {
    formik: {
      initialValues: {
        prefix: {
          company: "ACME",
          chamberOfCommerce: "12345678",
          street: "Bosmanlaan",
          number: "123",
          city: "Hamsterdam",
          postalCode: "1017 AB",
          country: "N",
        },
      },
      initialTouched: {
        prefix: {
          company: true,
          chamberOfCommerce: true,
          street: true,
          number: true,
          city: true,
          postalCode: true,
          country: true,
        },
      },
    },
  },
};

export const WithErrors: Story = {
  parameters: {
    formik: {
      initialErrors: {
        prefix: {
          company: ["Something went horribly wrong!"],
          chamberOfCommerce: ["Something went horribly wrong!"],
          street: ["Something went horribly wrong!"],
          number: ["Something went horribly wrong!"],
          city: ["Something went horribly wrong!"],
          postalCode: ["Something went horribly wrong!"],
          country: ["Something went horribly wrong!"],
        },
      },
      initialTouched: {
        prefix: {
          company: true,
          chamberOfCommerce: true,
          street: true,
          number: true,
          city: true,
          postalCode: true,
          country: true,
        },
      },
    },
  },
};
