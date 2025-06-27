import 'bootstrap';
import React from 'react';
import {createRoot} from 'react-dom/client';
import {IntlProvider} from 'react-intl';

import {getIntlProviderProps} from '../../i18n';
import {ModelKitSelect} from './ModelKitSelect';

// mount the detected components, based on class name
const nodes = document.querySelectorAll('.model-kit-select');
const modalNode = document.getElementById('add-kit-modal');

getIntlProviderProps()
  .then(intlProviderProps => {
    for (const node of nodes) {
      const {label, allowMultiple, htmlname, selected} = node.dataset;

      // cast string to actual boolean
      const _allowMultiple = allowMultiple === 'true';
      const _selected = selected.length ? selected.split(',').map(id => parseInt(id, 10)) : [];

      // mount component in the DOM node
      createRoot(node).render(
        <IntlProvider {...intlProviderProps}>
          <ModelKitSelect
            modalNode={modalNode}
            label={label}
            allowMultiple={_allowMultiple}
            htmlName={htmlname}
            selected={_selected}
          />
        </IntlProvider>,
      );
    }
  })
  .catch(console.error);
