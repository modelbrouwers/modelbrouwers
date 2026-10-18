import clsx from 'clsx';
import {useField} from 'formik';
import {ReactNode, useId} from 'react';

import ErrorList from './ErrorList';

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
  appearance: 'plain' | 'buttons';
}

const RadioOption: React.FC<RadioOptionProps> = ({name, value, label, graphic, appearance}) => {
  const [field] = useField<string>({name, value, type: 'radio'});
  return (
    <label className={clsx('radio-option', {'radio-option--button': appearance === 'buttons'})}>
      <input type="radio" className="radio-option__input" {...field} />
      {appearance === 'buttons' && <span className="radio-option__graphic">{graphic}</span>}
      <span className="radio-option__label">{label}</span>
    </label>
  );
};

export interface RadioProps {
  name: string;
  label: ReactNode;
  options: Omit<RadioOptionProps, 'name' | 'appearance'>[];
  appearance?: 'plain' | 'buttons';
}

/**
 * Radio input(s) with a mobile-friendly UI.
 *
 * There is room for graphics for each radio option.
 */
const Radio: React.FC<RadioProps & JSX.IntrinsicElements['input']> = ({
  name,
  label,
  options,
  appearance = 'plain',
}) => {
  const labelId = useId();
  return (
    <div className="radio-group">
      <div id={labelId} className="radio-group__label">
        {label}
      </div>
      <div className="radio-group__options" role="group" aria-labelledby={labelId}>
        {options.map(option => (
          <RadioOption key={option.value} name={name} {...option} appearance={appearance} />
        ))}
        <ErrorList name={name} />
      </div>
    </div>
  );
};

export default Radio;
