import PropTypes from 'prop-types';

import {createModelKit} from '@/data/kits/modelkit';
import {parseScale} from '@/data/kits/scale';

import {FormField} from '../../components/forms/FormField.js';
import {RadioSelect} from '../../components/forms/RadioSelect';
import BoxartUpload from './BoxartUpload';
import CreateBrandSelect from './CreateBrandSelect';
import CreateScaleSelect from './CreateScaleSelect';

// see brouwers.kits.models.KitDifficulties
// TODO: inject this into the DOM and read from the DOM
const DIFFICULTY_CHOICES = [
  {value: '10', display: 'very easy'},
  {value: '20', display: 'easy'},
  {value: '30', display: 'medium'},
  {value: '40', display: 'hard'},
  {value: '50', display: 'very hard'},
];

const AddKitForm = ({
  brand = null,
  scale = null,
  name = '',
  kitNumber = '',
  difficulty,
  onChange,
}) => {
  const onSelectChange = (selectedOption, action) => {
    const {name} = action;
    const value = selectedOption ? selectedOption.option : null;
    onChange({name, value});
  };

  const onInputChange = event => {
    const {name, value} = event.target;
    onChange({name, value});
  };

  return (
    <div className="form-horizontal">
      <FormField htmlId="add-kit-brand" label="brand" required={true}>
        <CreateBrandSelect
          inputId="add-kit-brand"
          value={brand}
          onChange={value => onChange({name: 'brand', value})}
        />
      </FormField>
      <FormField htmlId="add-kit-scale" label="scale" required={true}>
        <CreateScaleSelect
          inputId="add-kit-scale"
          value={scale}
          onChange={value => onChange({name: 'scale', value})}
        />
      </FormField>
      <FormField htmlId="add-kit-name" label="name" required={true}>
        <input
          type="text"
          name="name"
          className="form-control"
          required
          value={name}
          placeholder="kit name"
          onChange={onInputChange}
          id="add-kit-name"
        />
      </FormField>
      <FormField htmlId="add-kit-number" label="kit number" required={false}>
        <input
          type="text"
          name="kit_number"
          className="form-control"
          value={kitNumber}
          placeholder="kit number"
          onChange={onInputChange}
          id="add-kit-number"
        />
      </FormField>

      <FormField htmlId="add-kit-box_image" label="box image" required={false}>
        <BoxartUpload
          onComplete={uploadResponse =>
            onChange({
              name: 'boxartUUID',
              value: uploadResponse.uuid,
            })
          }
        />
      </FormField>

      <RadioSelect
        htmlId="add-kit-difficulty"
        name="difficulty"
        label="difficulty"
        choices={DIFFICULTY_CHOICES}
        required={false}
        onChange={onInputChange}
        currentValue={difficulty}
      />
    </div>
  );
};

AddKitForm.propTypes = {
  onChange: PropTypes.func.isRequired,
  name: PropTypes.string,
  kitNumber: PropTypes.string,
  difficulty: PropTypes.string.isRequired,
};

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
  const onSubmit = async event => {
    event.preventDefault();
    const submitData = {
      brand: brand ? brand.id : null,
      scale: scale ? scale.id : null,
      name: name,
      kit_number: kitNumber || '',
      difficulty: difficulty,
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
    <form id={formId} onSubmit={onSubmit}>
      <AddKitForm
        brand={brand}
        scale={scale}
        name={name}
        kitNumber={kitNumber}
        difficulty={difficulty}
        onChange={onChange}
      />
    </form>
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

export {AddKitForm, ModelKitAdd};
