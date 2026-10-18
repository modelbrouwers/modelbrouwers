import PropTypes from 'prop-types';
import React from 'react';

import {createModelKit} from '@/data/kits/modelkit';
import AddKitForm from '@/kits/model-kit-select/AddKitForm';

const KitReviewKitAdd = ({onKitAdded, formId}) => {
  /**
   * Submit handler, invoked when the create form is submitted.
   * @param  {DOMEvent} event The submit event
   */
  const onSubmit = async values => {
    const {brand, scale, name, kit_number = '', boxartUUID, difficulty} = values;
    const submitData = {
      brand: brand ? brand.id : null,
      scale: scale ? scale.id : null,
      name,
      kit_number,
      difficulty,
      box_image_uuid: boxartUUID,
    };

    // submit to backend
    let kit;
    try {
      kit = await createModelKit(submitData);
    } catch (err) {
      // TODO: handle validation errors
      console.error(err);
    }

    // handle the different serializers in the backend
    kit.brand = brand;
    kit.scale = scale;
    onKitAdded(kit);
  };

  return <AddKitForm formId={formId} onSubmit={onSubmit} />;
};

KitReviewKitAdd.propTypes = {
  onKitAdded: PropTypes.func.isRequired,
  formId: PropTypes.string,
};

export default KitReviewKitAdd;
