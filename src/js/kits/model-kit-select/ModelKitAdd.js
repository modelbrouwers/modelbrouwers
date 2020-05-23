import React, { useContext } from "react";
import ReactDOM from "react-dom";
import PropTypes from "prop-types";
import classNames from "classnames";

import { Brand } from "../../data/kits/brand";
import { Scale } from "../../data/kits/scale";
import { ModalContext, KitSearchContext } from "./context";

const FormField = ({
    htmlId,
    label,
    required = false,
    labelGrid = "col-sm-4",
    fieldGrid = "col-sm-8",
    children
}) => {
    const labelClassNames = classNames("control-label", labelGrid, {
        required: required
    });
    return (
        <div className="form-group clearfix">
            <label
                id={`label_${htmlId}`}
                htmlFor={htmlId}
                className={labelClassNames}
            >
                {label}
            </label>
            <div className={fieldGrid}>{children}</div>
        </div>
    );
};

const ModalContent = ({ brand = null, scale = null, name = "" }) => {
    return (
        <div className="form-horizontal">
            <FormField htmlId="add-kit-brand" label="brand" required={true}>
                <input
                    type="text"
                    className="form-control"
                    defaultValue={brand ? `${brand.name}:${brand.id}` : ""}
                />
            </FormField>

            <FormField htmlId="add-kit-scale" label="scale" required={true}>
                <input
                    type="text"
                    className="form-control"
                    defaultValue={scale ? `${scale.__str__}:${scale.id}` : ""}
                />
            </FormField>

            <FormField htmlId="add-kit-name" label="name" required={true}>
                <input
                    type="text"
                    className="form-control"
                    defaultValue={name}
                />
            </FormField>
        </div>
    );
};

const ModelKitAdd = ({ brand = null, scale = null, name = "" }) => {
    const modalNode = useContext(ModalContext);
    return ReactDOM.createPortal(
        <ModalContent brand={brand} scale={scale} name={name} />,
        modalNode
    );
};

ModelKitAdd.propTypes = {
    brand: PropTypes.instanceOf(Brand),
    scale: PropTypes.instanceOf(Scale),
    name: PropTypes.string
};

export { ModelKitAdd };
