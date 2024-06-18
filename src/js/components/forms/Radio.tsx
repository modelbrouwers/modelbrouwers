import { ReactNode, useId } from "react";
import { useField } from "formik";

import ErrorList from "./ErrorList";

export interface RadioOptionProps {
  name: string;
  value: string;
  /**
   * Label content. This must be phrasing content.
   */
  label: ReactNode;
  /**
   * A graphic of some sort to display in the label.
   *
   * Ensure these are phrasing content, as it will be nested in a label tag.
   */
  graphic?: ReactNode;
}

const RadioOption: React.FC<RadioOptionProps> = ({
  name,
  value,
  label,
  graphic,
}) => {
  const [field] = useField<string>({ name, value, type: "radio" });

  return (
    <label className="radio-option">
      <input type="radio" className="radio-option__input" {...field} />
      <span className="radio-option__graphic">{graphic}</span>
      <span className="radio-option__label">{label}</span>
    </label>
  );
};

export interface RadioProps {
  name: string;
  label: ReactNode;
  options: Omit<RadioOptionProps, "name">[];
}

/**
 * Radio input(s) with a mobile-friendly UI.
 *
 * There is room for graphics for each radio option.
 */
const Radio: React.FC<RadioProps & JSX.IntrinsicElements["input"]> = ({
  name,
  label,
  options,
}) => {
  const labelId = useId();
  return (
    <>
      <div id={labelId} className="radio-group__label">
        {label}
      </div>
      <div className="radio-group" role="group" aria-labelledby={labelId}>
        {options.map((option) => (
          <RadioOption name={name} {...option} />
        ))}
        <ErrorList name={name} />
      </div>
    </>
  );
};

export default Radio;
