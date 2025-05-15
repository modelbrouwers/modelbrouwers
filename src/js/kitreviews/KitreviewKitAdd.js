import PropTypes from 'prop-types';
import React, {useContext} from 'react';
import {useEvent} from 'react-use';
import {useImmerReducer} from 'use-immer';

import {createModelKit} from '@/data/kits/modelkit';

import {AddKitForm} from '../kits/model-kit-select/ModelKitAdd';
import {ModalContext} from '../kits/model-kit-select/context';

const initialState = {
  brand: null,
  scale: null,
  name: '',
  kit_number: '',
  difficulty: '30',
  boxartUUID: null,
};

const reducer = (draft, action) => {
  switch (action.type) {
    case 'SET_CREATE_KIT_PARAM': {
      const {param, value} = action.payload;
      if (!value && draft[param]) {
        delete draft[param];
      } else if (value) {
        draft[param] = value;
      }
      break;
    }

    default:
      throw new Error(`Unknown action: ${action.type}`);
  }
};

const KitReviewKitAdd = ({onKitAdded}) => {
  const {modalForm} = useContext(ModalContext);
  const [{brand, scale, name, kit_number, difficulty, boxartUUID}, dispatch] = useImmerReducer(
    reducer,
    initialState,
  );

  /**
   * Handle create form input change
   * @param  {String} options.name  Parameter name that changed
   * @param  {String|Number|Object|Null} options.value Value of the parameter
   * @return {void}                Triggers state update
   */
  const onChange = ({name, value}) => {
    // pre-populate create data
    dispatch({
      type: 'SET_CREATE_KIT_PARAM',
      payload: {
        param: name,
        value: value,
      },
    });
  };

  /**
   * Submit handler, invoked when the create form is submitted.
   * @param  {DOMEvent} event The submit event
   */
  const onSubmit = async event => {
    event.preventDefault();

    const submitData = {
      brand: brand ? brand.id : null,
      scale: scale ? scale.id : null,
      name: name,
      kit_number: kit_number || '',
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
  useEvent('submit', onSubmit, modalForm);

  return (
    <AddKitForm
      brand={brand}
      scale={scale}
      name={name}
      kitNumber={kit_number}
      difficulty={difficulty}
      onChange={onChange}
    />
  );
};

KitReviewKitAdd.propTypes = {
  onKitAdded: PropTypes.func.isRequired,
};

export default KitReviewKitAdd;
