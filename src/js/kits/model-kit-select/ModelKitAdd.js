import PropTypes from 'prop-types';
import React, {useContext} from 'react';
import ReactDOM from 'react-dom';
import {useEvent} from 'react-use';

import {FormField} from '../../components/forms/FormField.js';
import {RadioSelect} from '../../components/forms/RadioSelect';
import {Brand, BrandConsumer} from '../../data/kits/brand';
import {ModelKitConsumer} from '../../data/kits/modelkit';
import {Scale, ScaleConsumer, cleanScale} from '../../data/kits/scale';
import BoxartUpload from './BoxartUpload';
import {brandOptionGetter, scaleOptionGetter} from './FilterForm';
import KitFieldSelect from './KitFieldSelect';
import {ModalContext} from './context';

// see brouwers.kits.models.KitDifficulties
// TODO: inject this into the DOM and read from the DOM
const DIFFICULTY_CHOICES = [
  {value: '10', display: 'very easy'},
  {value: '20', display: 'easy'},
  {value: '30', display: 'medium'},
  {value: '40', display: 'hard'},
  {value: '50', display: 'very hard'},
];

const brandConsumer = new BrandConsumer();
const scaleConsumer = new ScaleConsumer();
const kitConsumer = new ModelKitConsumer();

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
        <KitFieldSelect
          name="brand"
          consumer={brandConsumer}
          prepareQuery={inputValue => (inputValue ? {name: inputValue} : {})}
          optionGetter={brandOptionGetter}
          onChange={onSelectChange}
          value={brand}
        />
      </FormField>
      <FormField htmlId="add-kit-scale" label="scale" required={true}>
        <KitFieldSelect
          name="scale"
          consumer={scaleConsumer}
          prepareQuery={inputValue => (inputValue ? {scale: cleanScale(inputValue)} : {})}
          optionGetter={scaleOptionGetter}
          onChange={onSelectChange}
          value={scale}
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
  brand: PropTypes.instanceOf(Brand),
  scale: PropTypes.instanceOf(Scale),
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
}) => {
  const {modal, modalBody, modalForm} = useContext(ModalContext);

  const onSubmit = event => {
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
    kitConsumer
      .create(submitData)
      .then(kit => {
        // handle the different serializers in the backend
        kit.brand = brand;
        kit.scale = scale;
        // FIXME: legacy bootstrap
        modal.modal('hide');
        onKitAdded(kit);
      })
      .catch(errors => {
        console.log(errors);
        // TODO: handle validation errors
      });
  };

  useEvent('submit', onSubmit, modalForm);

  return ReactDOM.createPortal(
    <AddKitForm
      brand={brand}
      scale={scale}
      name={name}
      kitNumber={kitNumber}
      difficulty={difficulty}
      onChange={onChange}
    />,
    modalBody,
  );
};

ModelKitAdd.propTypes = {
  brand: PropTypes.instanceOf(Brand),
  scale: PropTypes.instanceOf(Scale),
  name: PropTypes.string,
  kitNumber: PropTypes.string,
  difficulty: PropTypes.string,
  boxartUUID: PropTypes.string,
  onChange: PropTypes.func.isRequired,
  onKitAdded: PropTypes.func.isRequired,
};

export {AddKitForm, ModelKitAdd};
