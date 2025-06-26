import 'bootstrap';
import 'jquery';
import {createRoot} from 'react-dom/client';
import {IntlProvider} from 'react-intl';

import {getIntlProviderProps} from '@/i18n.js';

import AddNewKitButton from './AddNewKitButton';
import Slider from './slider.js';

export default class Page {
  static init() {
    // slider for property ratings
    new Slider('input[type="range"]');

    this.initKitCreate();
  }

  static async initKitCreate() {
    const buttonNode = document.getElementById('find-kit-form__button-add-kit');
    const modalNode = document.getElementById('add-kit-modal');
    if (!buttonNode || !modalNode) return;

    const intlProps = await getIntlProviderProps();
    const root = createRoot(buttonNode);
    root.render(
      <IntlProvider {...intlProps}>
        <AddNewKitButton
          modalNode={modalNode}
          onKitAdded={kit => {
            window.location = kit.url_kitreviews;
          }}
        />
      </IntlProvider>,
    );
  }
}
