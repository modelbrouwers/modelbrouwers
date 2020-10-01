import React, { useState } from "react";
import PropTypes from "prop-types";
import AsyncCreatableSelect from 'react-select/async-creatable';


const KitFieldSelect = ({name, consumer, prepareQuery, optionGetter, onChange, value = null}) => {
    const loadOptions = (inputValue) => {
        const params = prepareQuery(inputValue);
        return consumer
            .filter(params)
            .then( objects => objects.map(optionGetter) )
            .catch(console.error);
    };

    const selectedValue = value ? optionGetter(value) : null;

    const onSelectChange = (option, meta) => {
        if (meta.action !== "create-option") {
            onChange(option, meta);
        } else {
            // create new instance in the backend
            consumer
                .fromRaw(option.value)
                .then( instance => {
                    const newOption = optionGetter(instance);
                    Object.assign(option, newOption);
                    onChange(option, meta);
                });
        }
    };

    return (
        <AsyncCreatableSelect
            name={name}
            defaultOptions
            loadOptions={loadOptions}
            isClearable
            isSearchable
            value={selectedValue}
            onChange={onSelectChange}
        />
    );
};

KitFieldSelect.propTypes = {
    name: PropTypes.string.isRequired,
    consumer: PropTypes.shape({
        list: PropTypes.func.isRequired,
        fromRaw: PropTypes.func.isRequired
    }).isRequired,
    prepareQuery: PropTypes.func.isRequired,
    optionGetter: PropTypes.func.isRequired,
    onChange: PropTypes.func.isRequired,
    value: PropTypes.object,
};

export default KitFieldSelect;
