import Nl from "../locale/locales/nl.json";
import En from "../locale/locales/en.json";
import De from "../locale/locales/de.json";
import localeEn from "react-intl/locale-data/en";
import localeNl from "react-intl/locale-data/nl";
import localeDe from "react-intl/locale-data/de";

export const getLocale = () =>
    document.querySelector("html").getAttribute("lang");

export const getMessages = locale => {
    const messages = { en: En, nl: Nl, de: De };
    return messages[locale];
};

export const locales = [...localeEn, ...localeDe, ...localeNl];
