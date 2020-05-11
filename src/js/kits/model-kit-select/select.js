import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';


const Select = (props) => {
    const { fetchOptions, onChange } = props;
    const [options, setOptions] = useState([{value: '', label: '(loading...)'}]);

    useEffect(() => {
        fetchOptions()
            .then(options => setOptions(options))
            .catch(console.error);
    }, []);

    return (
        <select onChange={ (event) => onChange(event.target.value) } className="form-control">
            { options.map(
                option => <option key={option.value} value={ option.value }>{ option.label }</option>)
            }
        </select>
    );
};

Select.propTypes = {
    fetchOptions: PropTypes.func.isRequired,
    onChange: PropTypes.func.isRequired,
};

export { Select };
