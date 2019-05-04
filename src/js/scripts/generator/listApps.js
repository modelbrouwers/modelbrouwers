const fs = require("fs");

module.exports = () => {
    const names = fs.readdirSync("src/js");
    return names.filter(name => name !== ".DS_Store" && !name.includes(".js"));
};
