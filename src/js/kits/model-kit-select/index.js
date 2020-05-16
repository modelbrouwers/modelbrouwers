import React from 'react';
import ReactDOM from 'react-dom';
import { IntlProvider } from "react-intl";

import { getLocale, getMessages } from '../../translations/utils';
import { ModelKitSelect } from './ModelKitSelect';

const locale = getLocale() || 'nl';
const messages = getMessages(locale);

// mount the detected components, based on class name
const nodes = document.querySelectorAll('.model-kit-select');

for (const node of nodes) {
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
        <IntlProvider locale={locale} messages={messages}>
            <ModelKitSelect
                label={label}
                allowMultiple={_allowMultiple}
                htmlName={htmlname}
                selected={_selected}
            />
        </IntlProvider>,
        node
    );
}
