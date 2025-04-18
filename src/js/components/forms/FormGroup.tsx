import clsx from 'clsx';

export interface FormGroupProps extends React.HTMLAttributes<HTMLDivElement> {
  children?: React.ReactNode;
}

const FormGroup: React.FC<FormGroupProps> = ({className, children}) => {
  return <div className={clsx('form-group', className)}>{children}</div>;
};

export default FormGroup;
