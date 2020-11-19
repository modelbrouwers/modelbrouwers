import React from "react";
import PropTypes from "prop-types";

import { Label } from "./Label";

const RadioSelectOptionValue = PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.number
]);

const RadioSelectOption = ({
    name,
    htmlId,
    index,
    value,
    display,
    checked,
    onChange
}) => {
    const id = `${htmlId}_${index}`;
    return (
        <li className="radio-select__option">
            <input
                type="radio"
                name={name}
                id={id}
                value={value}
                checked={checked}
                onChange={onChange}
            />
            <label htmlFor={id}>{display}</label>
        </li>
    );
};

RadioSelectOption.propTypes = {
    name: PropTypes.string.isRequired,
    htmlId: PropTypes.string.isRequired,
    index: PropTypes.number.isRequired,
    value: RadioSelectOptionValue.isRequired,
    display: PropTypes.string.isRequired,
    checked: PropTypes.bool.isRequired
};

const RadioSelect = ({
    name,
    label,
    htmlId,
    required,
    onChange,
    currentValue = null,
    choices = [],
    labelGrid = "col-sm-4",
    fieldGrid = "col-sm-8"
}) => {
    return (
        <div className="form-group clearfix">
            <Label
                label={label}
                htmlId={htmlId}
                required={required}
                labelGrid={labelGrid}
            />
            <div className={fieldGrid}>
                <ul id={htmlId} className="radio-select">
                    {choices.map((choice, index) => (
                        <RadioSelectOption
                            key={choice.value}
                            name={name}
                            htmlId={htmlId}
                            index={index}
                            checked={choice.value == currentValue}
                            onChange={onChange}
                            {...choice}
                        />
                    ))}
                </ul>
            </div>
        </div>
    );
};

RadioSelect.propTypes = {
    name: PropTypes.string.isRequired,
    label: PropTypes.string.isRequired,
    htmlId: PropTypes.string.isRequired,
    onChange: PropTypes.func.isRequired,
    currentValue: RadioSelectOptionValue,
    required: PropTypes.bool,
    choices: PropTypes.arrayOf(
        PropTypes.shape({
            value: RadioSelectOption.propTypes.value,
            display: RadioSelectOption.propTypes.display
        })
    ),
    labelGrid: PropTypes.string,
    fieldGrid: PropTypes.string
};

export { RadioSelect };
