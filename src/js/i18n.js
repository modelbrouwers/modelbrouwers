const loadLocaleData = async locale => {
  switch (locale) {
    case 'nl':
      return import('./locale/compiled/nl.json');
    case 'en':
      return import('./locale/compiled/en.json');
    case 'de':
      return import('./locale/compiled/de.json');
    default:
      if (locale.length === 5) {
        const localeData = await loadLocaleData(locale.substring(0, 2));
        return localeData;
      }
      return import('./locale/compiled/en.json');
  }
};

const getIntlProviderProps = async () => {
  const lang = getLocale();
  const messages = await loadLocaleData(lang);
  return {
    messages,
    locale: lang,
    defaultLocale: 'en',
  };
};

const getLocale = () => {
  const lang = document.querySelector('html').getAttribute('lang');
  return lang.substring(0, 2);
};

export {loadLocaleData, getIntlProviderProps, getLocale};
