import React from 'react';

import { ScaleConsumer } from '../../data/kits/scale';

import { Select } from './select';

const scaleConsumer = new ScaleConsumer();

const fetchOptions = () => {
    return scaleConsumer
        .list()
        .then(scales => {
            console.log(scales);
            const options = scales.map(scale => {
                return {
                    value: scale.id,
                    label: scale.__str__,
                };
            });
            return [{value: '', label: '---------'}].concat(options);
        });
};


const ScaleSelect = (props) => {
    return (
        <Select fetchOptions={fetchOptions} />
    );
};

export { ScaleSelect };
