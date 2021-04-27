import "jquery";
import "bootstrap";

import React from "react";
import ReactDOM from "react-dom";

import { ModalContext } from "../kits/model-kit-select/context";
import KitReviewKitAdd from "./KitreviewKitAdd";

import Slider from "./slider.js";

const onKitAdded = kit => {
    window.location = kit.url_kitreviews;
};

const onAddNewKitClick = (event, btnNode, modalContext) => {
    event.preventDefault();
    ReactDOM.render(
        <ModalContext.Provider value={modalContext}>
            <KitReviewKitAdd onKitAdded={onKitAdded} />
        </ModalContext.Provider>,
        modalContext.modalBody
    );
    modalContext.modal.modal("show");
};

export default class Page {
    static init() {
        // slider for property ratings
        new Slider('input[type="range"]');

        this.initKitCreate();
    }

    static initKitCreate() {
        const modalNode = document.getElementById("add-kit-modal");
        const modal = $(modalNode);
        const modalBody = modalNode
            ? modalNode.querySelector(".modal-body")
            : null;
        const modalForm = modalNode ? modalNode.querySelector("form") : null;

        const modalContext = { modal, modalBody, modalForm };
        const nodes = document.querySelectorAll(
            ".find-kit-form__button-add-kit"
        );
        for (const node of nodes) {
            node.addEventListener("click", event =>
                onAddNewKitClick(event, node, modalContext)
            );
        }
    }
}
