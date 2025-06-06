import React from 'react';
import {createRoot} from 'react-dom/client';
import {IntlProvider} from 'react-intl';

import {getIntlProviderProps} from '../i18n';
import GroupBuildInset from './groupbuilds/GroupBuildInset';

export default class App {
  static async init() {
    const insets = document.querySelectorAll('.gb-inset');
    if (!insets.length) return;

    const intlProviderProps = await getIntlProviderProps();
    for (const node of insets) {
      const id = parseInt(node.dataset.id, 10);
      createRoot(node).render(
        <IntlProvider {...intlProviderProps}>
          <GroupBuildInset id={id} />
        </IntlProvider>,
      );
    }
  }
}
