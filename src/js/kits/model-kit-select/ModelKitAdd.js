import React, { useContext } from "react";
import ReactDOM from "react-dom";
import PropTypes from "prop-types";

import { ModalContext } from "./context";

const ModalContent = () => {
    return "MODAL CONTENT";
};

const ModelKitAdd = () => {
    const modalNode = useContext(ModalContext);
    return ReactDOM.createPortal(<ModalContent />, modalNode);
};

ModelKitAdd.propTypes = {};

export { ModelKitAdd };
