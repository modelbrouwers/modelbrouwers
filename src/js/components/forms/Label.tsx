import clsx from 'clsx';

export interface LabelProps {
  label: string;
  htmlId: string;
  labelGrid?: string;
  required?: boolean;
}

const Label: React.FC<LabelProps> = ({label, htmlId, labelGrid = 'col-sm-4', required = false}) => (
  <label
    id={`label_${htmlId}`}
    htmlFor={htmlId}
    className={clsx('control-label', labelGrid, {
      required: required,
    })}
  >
    {label}
  </label>
);

export default Label;
