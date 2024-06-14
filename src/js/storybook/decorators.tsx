import type { Decorator } from "@storybook/react";
import { Formik } from "formik";

export const withFormik: Decorator = (Story, context) => {
  const isDisabled = context.parameters?.formik?.disable ?? false;
  if (isDisabled) {
    return <Story />;
  }
  const initialValues = context.parameters?.formik?.initialValues || {};
  const initialErrors = context.parameters?.formik?.initialErrors || {};
  const initialTouched = context.parameters?.formik?.initialTouched || {};
  const wrapForm = context.parameters?.formik?.wrapForm ?? false;
  return (
    <Formik
      initialValues={initialValues}
      initialErrors={initialErrors}
      initialTouched={initialTouched}
      enableReinitialize
      onSubmit={(values, formikHelpers) => console.log(values, formikHelpers)}
    >
      {wrapForm ? (
        <form id="storybook-withFormik-decorator-form">
          <Story />
        </form>
      ) : (
        <Story />
      )}
    </Formik>
  );
};
