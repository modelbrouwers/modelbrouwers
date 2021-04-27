import "bootstrap";

import React from "react";
import ReactDOM from "react-dom";
import { IntlProvider } from "react-intl";

import { getLocale, getMessages } from "../../translations/utils";
import { ModelKitSelect } from "./ModelKitSelect";

import { ModalContext } from "./context";

const locale = getLocale() || "nl";
const messages = getMessages(locale);

// mount the detected components, based on class name
const nodes = document.querySelectorAll(".model-kit-select");
const modalNode = document.getElementById("add-kit-modal");
const modal = $(modalNode);
const modalBody = modalNode ? modalNode.querySelector(".modal-body") : null;
const modalForm = modalNode ? modalNode.querySelector("form") : null;

for (const node of nodes) {
    const { label, allowMultiple, htmlname, selected } = node.dataset;

    // cast string to actual boolean
    const _allowMultiple = allowMultiple === "true";
    const _selected = selected.length
        ? selected.split(",").map(id => parseInt(id, 10))
        : [];

    // mount component in the DOM node
    ReactDOM.render(
        <IntlProvider locale={locale} messages={messages}>
            <ModalContext.Provider value={{ modal, modalBody, modalForm }}>
                <ModelKitSelect
                    label={label}
                    allowMultiple={_allowMultiple}
                    htmlName={htmlname}
                    selected={_selected}
                />
            </ModalContext.Provider>
        </IntlProvider>,
        node
    );
}
