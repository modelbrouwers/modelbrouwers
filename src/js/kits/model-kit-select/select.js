import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';


const Select = (props) => {
    const { fetchOptions } = props;
    const [options, setOptions] = useState([{value: '', label: '(loading...)'}]);

    useEffect(() => {
        fetchOptions()
            .then(options => setOptions(options))
            .catch(console.error);
    }, [fetchOptions]);

    return (
        <select onChange={console.log} className="form-control">
            { options.map(
                option => <option key={option.value} value={ option.value }>{ option.label }</option>)
            }
        </select>
    );
};

Select.propTypes = {
    fetchOptions: PropTypes.func.isRequired,
};

export { Select };
