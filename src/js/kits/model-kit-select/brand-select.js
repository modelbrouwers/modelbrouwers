import React from 'react';
import PropTypes from 'prop-types';

import { BrandConsumer } from '../../data/kits/brand';

import { Select } from './select';

const brandConsumer = new BrandConsumer();

const fetchOptions = () => {
    return brandConsumer
        .list()
        .then(brands => {
            const options = brands.map(brand => {
                return {
                    value: brand.id,
                    label: brand.name,
                };
            });
            return [{value: '', label: '---------'}].concat(options);
        });
};

const BrandSelect = (props) => {
    return (
        <Select fetchOptions={fetchOptions} {...props} />
    );
};

BrandSelect.propTyeps = {
    onChange: PropTypes.func.isRequired,
};

export { BrandSelect };
