import type { Meta, StoryObj } from "@storybook/react";
import { withFormik, withFormGroup } from "@/storybook/decorators";

import TextField from "./TextField";

export default {
  title: "Components / Forms / TextField",
  component: TextField,
  decorators: [withFormGroup, withFormik],
  args: {
    name: "example",
    label: "Example textfield",
  },
  parameters: {
    formik: {
      initialValues: {
        example: "initial value",
      },
    },
  },
} satisfies Meta<typeof TextField>;

type Story = StoryObj<typeof TextField>;

export const Default: Story = {
  name: "TextField",
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
