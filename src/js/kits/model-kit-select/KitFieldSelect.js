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

// TODO: fix defaultValue by (un)mounting the addkitform component at the right time
const KitFieldSelect = ({
    name,
    consumer,
    labelField,
    onChange,
    defaultValue = null
}) => {
    const [state, setState] = useState({
        value: defaultValue ? getOption(defaultValue, labelField) : null,
        options: []
    });

    const { loading } = useAsync(() => {
        const promise = loadOptions(consumer, labelField).then(options =>
            setState({ ...state, options })
        );
        return promise;
    }, []);

    const onOptionChange = (option, meta) => {
        const name = meta.name;

        switch (meta.action) {
            case "select-option":
                setState({ ...state, value: option });
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
                            options: [option].concat(state.options)
                        });
                        // notify upstream component
                        onChange({ target: { name, value: option.value } });
                    })
                    .catch(console.error);
                break;

            case "clear":
                setState({ ...state, value: null });
                onChange({ target: { name, value: null } });
                break;
        }
    };

    const { value, options } = state;
    return (
        <CreatableSelect
            name={name}
            isClearable
            isLoading={loading}
            value={value}
            options={options}
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
    defaultValue: PropTypes.object
};

export { KitFieldSelect };
