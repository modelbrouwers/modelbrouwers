import React from 'react';
import ReactDOM from 'react-dom';

import { ModelKitSelect } from './model-kit-select';

// mount the detected components, based on class name
const nodes = document.querySelectorAll('.model-kit-select');

Array.from(nodes).forEach(node => {
    const {
        label,
        allowMultiple,
        htmlname,
        selected,
    } = node.dataset;

    // cast string to actual boolean
    const _allowMultiple = allowMultiple === 'true';
    const _selected = selected.length ? selected.split(',').map(id => parseInt(id, 10)) : [];

    // mount component in the DOM node
    ReactDOM.render(
        <ModelKitSelect
            label={label}
            allowMultiple={_allowMultiple}
            htmlName={htmlname}
            selected={_selected}
        />,
        node
    );
});
