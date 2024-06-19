import type { Meta, StoryObj } from "@storybook/react";
import { withFormik } from "@/storybook/decorators";

import Select from "./Select";

type Option = {
  value: string;
  label: string;
};

export default {
  title: "Components / Forms / Select",
  component: Select<Option>,
  decorators: [withFormik],
  args: {
    name: "example",
    label: "Select an option",
    required: true,
    options: [
      { value: "one", label: "One" },
      { value: "two", label: "Two" },
    ],
  },
  parameters: {
    formik: {
      initialValues: {
        example: "two",
      },
    },
  },
} satisfies Meta<typeof Select<Option>>;

type Story = StoryObj<typeof Select<Option>>;

export const Default: Story = {};

export const Empty: Story = {
  parameters: {
    formik: {
      initialValues: {
        example: "",
      },
    },
  },
};

export const WithError: Story = {
  parameters: {
    formik: {
      initialTouched: {
        example: true,
      },
      initialErrors: {
        example: "Some error",
      },
    },
  },
};
