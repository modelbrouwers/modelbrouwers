import React from "react";
import PropTypes from "prop-types";
import { useAsync } from "react-use";

const EMPTY_OPTION = {
    value: "",
    label: "---------"
};

const LOADING_OPTION = {
    value: "",
    label: "(loading...)"
};

const fetchOptions = (consumer, optionGetter) => {
    return consumer.list().then(objects => {
        const options = objects.map(optionGetter);
        return [EMPTY_OPTION].concat(options);
    });
};

const AsyncSelect = ({ consumer, optionGetter, onChange }) => {
    const { loading, value } = useAsync(
        () => fetchOptions(consumer, optionGetter),
        []
    );
    const options = loading ? [LOADING_OPTION] : value;
    return (
        <select
            onChange={event => onChange(event.target.value)}
            className="form-control"
        >
            {options.map(option => (
                <option key={option.value} value={option.value}>
                    {option.label}
                </option>
            ))}
        </select>
    );
};

AsyncSelect.propTypes = {
    consumer: PropTypes.shape({
        list: PropTypes.func.isRequired
    }).isRequired,
    optionGetter: PropTypes.func.isRequired,
    onChange: PropTypes.func.isRequired
};

export { AsyncSelect };