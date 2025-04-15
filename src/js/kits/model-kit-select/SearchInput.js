import PropTypes from 'prop-types';
import React, {useState} from 'react';
import {FormattedMessage} from 'react-intl';

const SearchInput = ({onChange}) => {
  const [query, setQuery] = useState('');
  return (
    <FormattedMessage id="kits.filter.byName" defaultMessage="filter by name">
      {placeholder => (
        <input
          type="text"
          className="form-control"
          value={query}
          onChange={event => {
            const newQuery = event.target.value;
            setQuery(newQuery);
            onChange(event);
          }}
          placeholder={placeholder}
        />
      )}
    </FormattedMessage>
  );
};

SearchInput.propTypes = {
  onChange: PropTypes.func.isRequired,
};

export {SearchInput};
