import React from "react";

const ModalContext = React.createContext({
    modal: null,
    modalBody: null,
    modalForm: null
});

export { ModalContext };
