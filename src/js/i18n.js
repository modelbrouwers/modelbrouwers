const loadLocaleData = (locale) => {
    switch (locale) {
        case "nl":
        case "en":
        case "de":
            return import(`./locale/compiled/${locale}.json`);
        default:
            console.error(`Unsupported locale: ${locale}`);
            return import("./locale/compiled/en.json");
    }
};

const getIntlProviderProps = async () => {
    const lang = document.querySelector("html").getAttribute("lang");
    const messages = await loadLocaleData(lang);
    return {
        messages,
        locale: lang,
        defaultLocale: "en",
    };
};

export { loadLocaleData, getIntlProviderProps };
