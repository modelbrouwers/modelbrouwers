import { useId } from "react";
import { useField } from "formik";
import clsx from "clsx";

import ErrorList from "./ErrorList";

interface TextFieldProps {
  name: string;
  label: string;
}

const TextField: React.FC<TextFieldProps & JSX.IntrinsicElements["input"]> = ({
  name,
  label,
  className: _className,
  ...props
}) => {
  const id = useId();
  const [field] = useField<string>(name);
  const className = clsx("form-control", _className);
  return (
    <>
      {label && (
        <label
          htmlFor={id}
          className={clsx("control-label", { required: props.required })}
        >
          {label}
        </label>
      )}
      <input type="text" id={id} className={className} {...field} {...props} />
      <ErrorList name={name} />
    </>
  );
};

export default TextField;
