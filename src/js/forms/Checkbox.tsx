import { ReactNode, useId } from "react";
import { useField } from "formik";

import ErrorList from "./ErrorList";

export interface CheckboxProps {
  name: string;
  label: ReactNode;
}

const TextField: React.FC<CheckboxProps & JSX.IntrinsicElements["input"]> = ({
  name,
  label,
  ...props
}) => {
  const id = useId();
  const [field] = useField({ name, type: "checkbox" });
  return (
    <div className="form-check checkbox-flex">
      <input
        type="checkbox"
        id={id}
        className="form-check-input"
        {...field}
        {...props}
      />
      <label htmlFor={id} className="form-check-label">
        {label}
      </label>
      <ErrorList name={name} />
    </div>
  );
};

export default TextField;
