import PropTypes from 'prop-types';

import {createModelKit} from '@/data/kits/modelkit';

import AddKitForm from './AddKitForm';

const ModelKitAdd = ({
  brand,
  scale,
  name,
  kitNumber,
  difficulty = '30',
  boxartUUID = null,
  onChange,
  onKitAdded,
  formId,
}) => {
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

  return (
    <AddKitForm
      formId={formId}
      onSubmit={onSubmit}
      initialValues={{
        brand,
        scale,
        name,
        kit_number: kitNumber ?? '',
        difficulty,
      }}
    />
  );
};

ModelKitAdd.propTypes = {
  name: PropTypes.string,
  kitNumber: PropTypes.string,
  difficulty: PropTypes.string,
  boxartUUID: PropTypes.string,
  onChange: PropTypes.func.isRequired,
  onKitAdded: PropTypes.func.isRequired,
};

export {ModelKitAdd};
