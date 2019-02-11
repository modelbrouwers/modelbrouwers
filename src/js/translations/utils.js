import Nl from "../locale/locales/nl.json";
import En from "../locale/locales/en.json";
import De from "../locale/locales/de.json";

export const getLocale = () =>
    document.querySelector("html").getAttribute("lang");

export const getMessages = locale => {
    const messages = { en: En, nl: Nl, de: De };
    return messages[locale];
};
