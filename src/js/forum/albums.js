import insertTextAtCursor from 'insert-text-at-cursor';
import React from 'react';
import {createRoot} from 'react-dom/client';
import {IntlProvider} from 'react-intl';

import {getIntlProviderProps} from '../i18n';
import SideBar from './albums/SideBar';

export default class App {
  static init() {
    // check if we're in posting mode
    const textArea = document.querySelector('textarea[name="message"],textarea[name="signature"]');
    if (!textArea) return;

    const mountNode = document.createElement('div');
    document.body.appendChild(mountNode);

    const insertPhoto = bbcode => {
      insertTextAtCursor(textArea, bbcode + '\n');
    };

    getIntlProviderProps()
      .then(intlProviderProps => {
        createRoot(mountNode).render(
          <IntlProvider {...intlProviderProps}>
            <SideBar onInsertPhoto={insertPhoto} />
          </IntlProvider>,
        );
      })
      .catch(console.error);
  }
}
