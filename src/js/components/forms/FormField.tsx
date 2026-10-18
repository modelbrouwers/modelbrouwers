import Label from './Label';

export interface FormFieldProps {
  children: React.ReactNode;
  htmlId: string;
  label: string;
  required?: boolean;
  labelGrid?: string;
  fieldGrid?: string;
}

const FormField: React.FC<FormFieldProps> = ({
  htmlId,
  label,
  required = false,
  labelGrid = 'col-sm-4',
  fieldGrid = 'col-sm-8',
  children,
}) => {
  return (
    <div className="form-group clearfix">
      <Label label={label} htmlId={htmlId} required={required} labelGrid={labelGrid} />
      <div className={fieldGrid}>{children}</div>
    </div>
  );
};

export default FormField;
