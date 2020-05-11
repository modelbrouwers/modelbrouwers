import React, { useState } from 'react';
import { FormattedMessage } from 'react-intl';
import PropTypes from 'prop-types';


const SearchInput = (props) => {
    const { onChange } = props;
    const [query, setQuery] = useState('');
    return (
        <FormattedMessage
            id="kits.filter.byName"
            defaultMessage="filter by name">
            {
                placeholder =>
                    <input
                        type="text"
                        className="form-control"
                        value={query}
                        onChange={(event) => {
                            const newQuery = event.target.value;
                            setQuery(newQuery);
                            onChange(newQuery);
                        }}
                        placeholder={placeholder}
                    />
            }
        </FormattedMessage>

    );
};

SearchInput.propTypes = {
    onChange: PropTypes.func.isRequired,
}

export { SearchInput };
