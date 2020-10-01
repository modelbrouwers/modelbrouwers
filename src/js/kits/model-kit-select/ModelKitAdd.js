import React, { useContext, useState } from "react";
import ReactDOM from "react-dom";
import PropTypes from "prop-types";

import { FormField } from "../../components/forms/FormField";
import { RadioSelect } from "../../components/forms/RadioSelect";

import { Brand, BrandConsumer } from "../../data/kits/brand";
import { Scale, ScaleConsumer } from "../../data/kits/scale";
import { ModalContext, KitSearchContext } from "./context";
import { KitFieldSelect } from "./KitFieldSelect";

// see brouwers.kits.models.KitDifficulties
// TODO: inject this into the DOM and read from the DOM
const DIFFICULTY_CHOICES = [
    { value: 10, display: "very easy" },
    { value: 20, display: "easy" },
    { value: 30, display: "medium" },
    { value: 40, display: "hard" },
    { value: 50, display: "very hard" }
];

const brandConsumer = new BrandConsumer();
const scaleConsumer = new ScaleConsumer();

const AddKitForm = ({ dispatch, brand = null, scale = null, name = "" }) => {

    const onNewKitDefaultChange = (event) => {
        // console.log(event);
        const { name, value } = event.target;
        dispatch({
            type: 'SET_NEW_KIT_PARAM',
            payload: {
                param: name,
                target: event.target,
            }
        });
    };

    const onChange = event => {
        console.log(name, value);
    };

    return null;

    return (
        <div className="form-horizontal">
            <FormField htmlId="add-kit-brand" label="brand" required={true}>
                <KitFieldSelect
                    name="brand"
                    consumer={brandConsumer}
                    labelField="name"
                    onChange={onNewKitDefaultChange}
                    value={brand}
                />
            </FormField>
            <FormField htmlId="add-kit-scale" label="scale" required={true}>
                <KitFieldSelect
                    name="scale"
                    consumer={scaleConsumer}
                    labelField="__str__"
                    onChange={onNewKitDefaultChange}
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
                    onChange={onChange}
                />
            </FormField>
            <FormField
                htmlId="add-kit-number"
                label="kit number"
                required={false}
            >
                <input
                    type="text"
                    name="kit_number"
                    className="form-control"
                    value=""
                    placeholder="kit number"
                    onChange={onChange}
                />
            </FormField>

            {/* TODO: box image */}

            <RadioSelect
                htmlId="add-kit-difficulty"
                name="difficulty"
                label="difficulty"
                choices={DIFFICULTY_CHOICES}
                required={false}
                onChange={onChange}
                currentValue=""
            />
        </div>
    );
};

const ModelKitAdd = ({ dispatch, brand = null, scale = null, name = "" }) => {
    const modalNode = useContext(ModalContext);
    return ReactDOM.createPortal(
        <AddKitForm dispatch={dispatch} brand={brand} scale={scale} name={name} />,
        modalNode
    );
};

ModelKitAdd.propTypes = {
    dispatch: PropTypes.func.isRequired,
    brand: PropTypes.instanceOf(Brand),
    scale: PropTypes.instanceOf(Scale),
    name: PropTypes.string,
};

export { ModelKitAdd };
