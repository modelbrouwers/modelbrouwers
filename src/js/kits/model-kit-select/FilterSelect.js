import PropTypes from 'prop-types';
import React from 'react';
import AsyncSelect from 'react-select/async';

const FilterSelect = ({name, consumer, optionGetter, onChange}) => {
  const loadOptions = () => {
    return consumer
      .list()
      .then(objects => objects.map(optionGetter))
      .catch(console.error);
  };

  return (
    <AsyncSelect
      name={name}
      defaultOptions
      loadOptions={loadOptions}
      isClearable
      isSearchable={false}
      onChange={onChange}
    />
  );
};

FilterSelect.propTypes = {
  name: PropTypes.string.isRequired,
  consumer: PropTypes.shape({
    list: PropTypes.func.isRequired,
  }).isRequired,
  optionGetter: PropTypes.func.isRequired,
  onChange: PropTypes.func.isRequired,
};

export default FilterSelect;
