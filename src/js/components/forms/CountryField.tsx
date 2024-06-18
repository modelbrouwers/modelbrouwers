import clsx from "clsx";
import { useField } from "formik";
import { ReactNode, useId } from "react";
import Select, { Props, GroupBase } from "react-select";
import { useIntl } from "react-intl";
import countries from "i18n-iso-countries";

import ErrorList from "./ErrorList";
import FormGroup from "./FormGroup";

// TODO: can we split this in the bundle?
countries.registerLocale(require("i18n-iso-countries/langs/en.json"));
countries.registerLocale(require("i18n-iso-countries/langs/nl.json"));
countries.registerLocale(require("i18n-iso-countries/langs/de.json"));

export interface CountryOption {
  value: "N" | "B" | "D";
  label: string;
}

export interface CountryFieldProps {
  name: string;
  label: ReactNode;
}

const SUPPORTED_COUNTRIES = {
  N: (lang: string) => countries.getName("NL", lang),
  B: (lang: string) => countries.getName("BE", lang),
  D: (lang: string) => countries.getName("DE", lang),
};

const CountryField: React.FC<
  CountryFieldProps & Props<CountryOption, false, GroupBase<CountryOption>>
> = ({ name, label, ...props }) => {
  const intl = useIntl();
  const id = useId();
  const [{ value, ...field }, , helpers] = useField<
    CountryOption["value"] | undefined
  >(name);

  // build localized list of country names
  const langCode = intl.locale.split("-")[0];
  const countryOptions = Object.entries(SUPPORTED_COUNTRIES).map(
    ([value, nameGetter]) => ({
      value: value as keyof typeof SUPPORTED_COUNTRIES,
      label: nameGetter(langCode),
    }),
  );

  const selectedOption = countryOptions.find(
    (option) => option.value === value,
  );

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
      <Select<CountryOption, false>
        id={id}
        options={countryOptions}
        className=""
        value={selectedOption}
        {...field}
        onChange={(option: CountryOption | null) => {
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
};

export default CountryField;
