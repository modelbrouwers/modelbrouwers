const manageTranslations = require("react-intl-translations-manager").default;

manageTranslations({
    messagesDirectory: "src/js/translations/messages",
    translationsDirectory: "src/js/translations/locales",
    languages: ["en", "nl", "de"]
});
