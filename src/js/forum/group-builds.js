"use strict";

import Handlebars from "../general/hbs-pony";

import { GroupBuildConsumer } from "../data/group-build";

const render = (gb, node) => {
    Handlebars.render("groupbuilds::inset", gb, $(node)).catch(console.error);
};

export default class App {
    static init() {
        const consumer = new GroupBuildConsumer();
        const insets = document.querySelectorAll(".gb-inset");

        insets.forEach(node => {
            consumer
                .read(node.dataset.id)
                .then(gb => render(gb, node))
                .catch(console.error);
        });
    }
}
