import Label from './Label';

export interface FormFieldProps {
  children: React.ReactNode;
  htmlId: string;
  label: string;
  required?: boolean;
  labelGrid?: string;
  fieldGrid?: string;
}

const FormField: React.FC<FormFieldProps> = ({htmlId, label, required = false, children}) => {
  return (
    <div className="form-field">
      <Label label={label} htmlId={htmlId} required={required} labelGrid="" />
      <div>{children}</div>
    </div>
  );
};

export default FormField;
