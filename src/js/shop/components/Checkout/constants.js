import countries from "i18n-iso-countries";

import { getLocale } from "../../../i18n";

countries.registerLocale(require("i18n-iso-countries/langs/en.json"));
countries.registerLocale(require("i18n-iso-countries/langs/nl.json"));
countries.registerLocale(require("i18n-iso-countries/langs/de.json"));

const lang = getLocale().split("-")[0];

// Map country translated names to their weird abbreviations from backend
export const SUPPORTED_COUNTRIES = {
    N: countries.getName("NL", lang),
    B: countries.getName("BE", lang),
    D: countries.getName("DE", lang),
};
export const country_list = Object.keys(SUPPORTED_COUNTRIES).map((key) => ({
    label: SUPPORTED_COUNTRIES[key],
    value: key,
}));

export const CHECKOUT_MODES = ["withoutAccount", "withAccount"];

export const EMPTY_ADDRESS = {
    company: "",
    chamberOfCommerce: "",
    street: "",
    number: "",
    city: "",
    postalCode: "",
    country: "N",
};
