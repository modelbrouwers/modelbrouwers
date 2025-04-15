import clsx from 'clsx';
import {useField} from 'formik';
import {ReactNode, useId} from 'react';

import ErrorList from './ErrorList';
import FormGroup, {FormGroupProps} from './FormGroup';

export interface TextFieldProps {
  name: string;
  label: ReactNode;
  formGroupProps?: FormGroupProps;
}

const TextField: React.FC<TextFieldProps & JSX.IntrinsicElements['input']> = ({
  name,
  label,
  className: _className,
  formGroupProps,
  ...props
}) => {
  const id = useId();
  const [field] = useField<string>(name);
  const className = clsx('form-control', _className);
  return (
    <FormGroup {...formGroupProps}>
      {label && (
        <label htmlFor={id} className={clsx('control-label', {required: props.required})}>
          {label}
        </label>
      )}
      <input type="text" id={id} className={className} {...field} {...props} />
      <ErrorList name={name} />
    </FormGroup>
  );
};

export default TextField;
