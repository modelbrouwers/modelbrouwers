import clsx from "clsx";
import { useField } from "formik";
import { ReactNode, useId } from "react";
import { default as ReactSelect, Props, GroupBase } from "react-select";

import ErrorList from "./ErrorList";
import FormGroup from "./FormGroup";

interface BaseOption {
  value: string | number;
}

export interface SelectProps<T extends BaseOption> {
  name: string;
  label: ReactNode;
  options: T[];
}

function Select<T extends BaseOption>({
  name,
  label,
  options,
  ...props
}: SelectProps<T> & Props<T, false, GroupBase<T>>) {
  const id = useId();
  const [{ value, ...field }, , helpers] = useField<T["value"] | undefined>(
    name,
  );
  const selectedOption = options.find((option) => option.value === value);
  return (
    <FormGroup>
      {label && (
        <label
          htmlFor={id}
          className={clsx("control-label", { required: props.required })}
        >
          {label}
        </label>
      )}
      <ReactSelect<T, false>
        id={id}
        options={options}
        className=""
        value={selectedOption}
        {...field}
        onChange={(option: T | null) => {
          if (option === null) {
            helpers.setValue(undefined);
            return;
          }
          helpers.setValue(option.value);
        }}
        {...props}
      />
      <ErrorList name={name} />
    </FormGroup>
  );
}

export default Select;
