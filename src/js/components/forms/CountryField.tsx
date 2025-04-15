import countries from 'i18n-iso-countries';
import {ComponentProps, ReactNode} from 'react';
import {IntlShape, useIntl} from 'react-intl';

import Select from './Select';

// TODO: can we split this in the bundle?
countries.registerLocale(require('i18n-iso-countries/langs/en.json'));
countries.registerLocale(require('i18n-iso-countries/langs/nl.json'));
countries.registerLocale(require('i18n-iso-countries/langs/de.json'));

const SUPPORTED_COUNTRIES = {
  N: (lang: string) => countries.getName('NL', lang),
  B: (lang: string) => countries.getName('BE', lang),
  D: (lang: string) => countries.getName('DE', lang),
};

export const getCountryName = (
  intl: IntlShape,
  country: keyof typeof SUPPORTED_COUNTRIES,
): string => {
  const langCode = intl.locale.split('-')[0];
  return SUPPORTED_COUNTRIES[country](langCode);
};

export interface CountryOption {
  value: 'N' | 'B' | 'D';
  label: string;
}

export interface CountryFieldProps {
  name: string;
  label: ReactNode;
}

type SelectProps = Omit<ComponentProps<typeof Select<CountryOption>>, 'options'>;

const CountryField: React.FC<CountryFieldProps & SelectProps> = ({name, label, ...props}) => {
  const intl = useIntl();
  // build localized list of country names
  const langCode = intl.locale.split('-')[0];
  const countryOptions = Object.entries(SUPPORTED_COUNTRIES).map(([value, nameGetter]) => ({
    value: value as keyof typeof SUPPORTED_COUNTRIES,
    label: nameGetter(langCode),
  }));
  return <Select<CountryOption> name={name} label={label} options={countryOptions} {...props} />;
};

export default CountryField;
