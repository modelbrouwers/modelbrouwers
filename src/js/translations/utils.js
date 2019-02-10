import Nl from "./locales/nl.json";
import En from "./locales/en.json";
import De from "./locales/de.json";

export const getLocale = () =>
    document.querySelector("html").getAttribute("lang");

export const getMessages = locale => {
    const messages = { en: En, nl: Nl, de: De };
    return messages[locale];
};
