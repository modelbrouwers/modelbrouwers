import React, { useState } from "react";
import { useAsync, useDebounce } from "react-use";
import PropTypes from "prop-types";
import CreatableSelect from "react-select/creatable";

import { Brand, BrandConsumer } from "../../data/kits/brand";

const brandConsumer = new BrandConsumer();

const getOption = brand => {
    return {
        value: brand.id,
        label: brand.name
    };
};

const loadOptions = () => {
    return brandConsumer
        .list()
        .then(brands => brands.map(brand => getOption(brand)))
        .catch(console.error);
};

const BrandAutocomplete = ({ onChange, brand = null }) => {
    const [state, setState] = useState({
        value: brand ? getOption(brand) : null,
        options: []
    });

    const { loading } = useAsync(
        () => loadOptions().then(options => setState({ ...state, options })),
        []
    );

    const onOptionChange = (option, meta) => {
        const name = meta.name;

        switch (meta.action) {
            case "select-option":
                setState({ ...state, value: option });
                onChange({ target: { name, value: option.value } });
                break;

            case "create-option":
                // create brand in the backend
                brandConsumer
                    .fromRaw(option.value)
                    .then(brand => {
                        option.value = brand.id;
                        setState({
                            value: option,
                            options: [option].concat(state.options)
                        });
                        // notify upstream component
                        onChange({ target: { name, value: option.value } });
                    })
                    .catch(console.error);
                break;
        }
    };

    const { value, options } = state;
    return (
        <CreatableSelect
            name="brand"
            isClearable
            isLoading={loading}
            value={value}
            options={options}
            onChange={onOptionChange}
        />
    );
};

BrandAutocomplete.propTypes = {
    onChange: PropTypes.func.isRequired,
    brand: PropTypes.instanceOf(Brand)
};

export { BrandAutocomplete };
