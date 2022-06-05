import React from "react";
import PropTypes from "prop-types";
import classNames from "classnames";

// TODO: merge with components/forms/FormField.js
const FormField = ({
    name,
    label: labelText = "",
    component: Component = "input",
    id = "",
    ...props
}) => {
    const isRequired = props.required || false;
    const labelId = `label_${name}`;
    const fieldId = id || `id_${name}`;
    const label = labelText ? (
        <label
            id={labelId}
            htmlFor={fieldId}
            className={classNames("control-label", { required: isRequired })}
        >
            {labelText}
        </label>
    ) : null;

    const inputProps = { className: "form-control" };
    if (Component === "input" && !inputProps.type) {
        inputProps.type = "text";
    }
    if (labelText) {
        inputProps["aria-labelledby"] = labelId;
    }

    return (
        <>
            {label}
            <Component name={name} id={fieldId} {...inputProps} {...props} />
        </>
    );
};

FormField.propTypes = {
    name: PropTypes.string.isRequired,
    label: PropTypes.node,
    id: PropTypes.string,
    component: PropTypes.oneOfType([PropTypes.elementType, PropTypes.string]),
};

const FormGroup = ({ extraClassName = "", children }) => {
    const className = classNames("form-group", extraClassName);
    return <div className={className}>{children}</div>;
};

FormGroup.propTypes = {
    extraClassName: PropTypes.string,
    children: PropTypes.node,
};

export default FormField;
export { FormField, FormGroup };
