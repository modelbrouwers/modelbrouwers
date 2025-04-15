import type {Decorator} from '@storybook/react';
import {Formik} from 'formik';

export const withFormik: Decorator = (Story, context) => {
  const isDisabled = context.parameters?.formik?.disable ?? false;
  if (isDisabled) {
    return <Story />;
  }

  const formikParams = context.parameters?.formik;

  const initialValues = formikParams?.initialValues || {};
  const initialErrors = formikParams?.initialErrors || {};
  const initialTouched = formikParams?.initialTouched || {};
  const wrapForm = formikParams?.wrapForm ?? false;
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
