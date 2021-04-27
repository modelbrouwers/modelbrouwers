const manageTranslations = require("react-intl-translations-manager").default;

manageTranslations({
    messagesDirectory: "src/js/locale/messages",
    translationsDirectory: "src/js/locale/locales",
    languages: ["en", "nl", "de"]
});
