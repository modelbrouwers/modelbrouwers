import React, { useState } from "react";
import PropTypes from "prop-types";
import AsyncCreatableSelect from "react-select/async-creatable";

import { Brand, BrandConsumer } from "../../data/kits/brand";

const brandConsumer = new BrandConsumer();

const loadOptions = inputValue => {
    if (inputValue.length && inputValue.length < 3) {
        return Promise.resolve([]);
    }

    return brandConsumer
        .filter({ name: inputValue })
        .then(brands =>
            brands.map(brand => {
                return { value: brand.id, label: brand.name };
            })
        )
        .catch(console.error);
};

const BrandAutocomplete = ({ onChange, brand = null }) => {
    const onOptionChange = (option, meta) => {
        const name = meta.name;

        switch (meta.action) {
            case "select-option":
                onChange({ target: { name, value: option.value } });
                break;
            case "create-option":
                // create brand in the backend
                brandConsumer
                    .fromRaw(option.value)
                    .then(brand => {
                        option.value = brand.id;
                        // notify upstream component
                        onChange({ target: { name, value: option.value } });
                    })
                    .catch(console.error);
                break;
        }
    };

    return (
        <AsyncCreatableSelect
            name="brand"
            defaultValue={brand ? brand.id : null}
            defaultInputValue={brand ? brand.name : ""}
            onChange={onOptionChange}
            cacheOptions
            defaultOptions
            loadOptions={loadOptions}
        />
    );
};

BrandAutocomplete.propTypes = {
    onChange: PropTypes.func.isRequired,
    brand: PropTypes.instanceOf(Brand)
};

export { BrandAutocomplete };
