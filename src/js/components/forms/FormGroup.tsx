import clsx from 'clsx';
import {PropsWithChildren} from 'react';

export type FormGroupProps = PropsWithChildren<JSX.IntrinsicElements['div']>;

const FormGroup: React.FC<FormGroupProps> = ({className, children}) => {
  return <div className={clsx('form-group', className)}>{children}</div>;
};

export default FormGroup;
