import deMessages from '../src/js/locale/compiled/de.json';
import enMessages from '../src/js/locale/compiled/en.json';
import nlMessages from '../src/js/locale/compiled/nl.json';

// Populate the messages object
const messages = {
  nl: nlMessages,
  en: enMessages,
  de: deMessages,
};

const formats = {}; // optional, if you have any formats

export const reactIntl = {
  defaultLocale: 'en',
  locales: Object.keys(messages),
  messages,
  formats,
};
