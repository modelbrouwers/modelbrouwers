import React, { useState } from "react";
import { useAsync, useDebounce } from "react-use";
import PropTypes from "prop-types";
import CreatableSelect from "react-select/creatable";

const getOption = (object, labelField) => {
    return {
        value: object.id,
        label: object[labelField]
    };
};

const loadOptions = (consumer, labelField) => {
    return consumer
        .list()
        .then(objectList =>
            objectList.map(object => getOption(object, labelField))
        )
        .catch(console.error);
};

const KitFieldSelect = ({
    name,
    consumer,
    labelField,
    onChange,
    value = null
}) => {

    console.log(value);

    const state = useAsync(
        () => loadOptions(consumer, labelField),
        []
    );

    const selectValue = value ? getOption(value, labelField) : null;

    const onOptionChange = (option, meta) => {
        const name = meta.name;

        switch (meta.action) {
            case "select-option":
                onChange({ target: { name, value: option.value } });
                break;

            case "create-option":
                // create new instance in the backend
                consumer
                    .fromRaw(option.value)
                    .then(newObject => {
                        option.value = newObject.id;
                        setState({
                            value: option,
                            options: [option].concat(state.value)
                        });
                        // notify upstream component
                        onChange({ target: { name, value: option.value } });
                    })
                    .catch(console.error);
                break;

            case "clear":
                onChange({ target: { name, value: null } });
                break;
        }
    };

    const { error, loading } = state;
    return (
        <CreatableSelect
            name={name}
            isClearable
            isLoading={loading}
            value={selectValue}
            options={state.value}
            onChange={onOptionChange}
        />
    );
};

KitFieldSelect.propTypes = {
    name: PropTypes.string.isRequired,
    consumer: PropTypes.shape({
        list: PropTypes.func.isRequired,
        fromRaw: PropTypes.func.isRequired
    }).isRequired,
    labelField: PropTypes.string.isRequired,
    onChange: PropTypes.func.isRequired,
    value: PropTypes.object
};

export { KitFieldSelect };
