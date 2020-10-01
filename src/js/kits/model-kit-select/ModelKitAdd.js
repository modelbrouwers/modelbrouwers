import React, { useContext } from "react";
import ReactDOM from "react-dom";
import PropTypes from "prop-types";
import { useEvent } from "react-use";

import { FormField } from "../../components/forms/FormField";
import { RadioSelect } from "../../components/forms/RadioSelect";

import { Brand, BrandConsumer } from "../../data/kits/brand";
import { Scale, ScaleConsumer, cleanScale } from "../../data/kits/scale";
import { ModalContext, KitSearchContext } from "./context";
import { brandOptionGetter, scaleOptionGetter } from './FilterForm';
import KitFieldSelect from "./KitFieldSelect";

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

const AddKitForm = ({
    brand = null,
    scale = null,
    name = "",
    kitNumber="",
    difficulty=null,
    onChange,
    children
}) => {

    const onSelectChange = (selectedOption, action) => {
        const {name} = action;
        const value = selectedOption ? selectedOption.option : null;
        onChange({name, value});
    };

    const onInputChange = (event) => {
        const {name, value} = event.target;
        onChange({name, value});
    };

    return (
        <div className="form-horizontal">
            <FormField htmlId="add-kit-brand" label="brand" required={true}>
                <KitFieldSelect
                    name="brand"
                    consumer={brandConsumer}
                    prepareQuery={ inputValue => inputValue ? {name: inputValue} : {} }
                    optionGetter={brandOptionGetter}
                    onChange={onSelectChange}
                    value={brand}
                />
            </FormField>
            <FormField htmlId="add-kit-scale" label="scale" required={true}>
                <KitFieldSelect
                    name="scale"
                    consumer={scaleConsumer}
                    prepareQuery={ inputValue => inputValue ? {scale: cleanScale(inputValue)} : {} }
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

            {/* TODO: box image */}

            <RadioSelect
                htmlId="add-kit-difficulty"
                name="difficulty"
                label="difficulty"
                choices={DIFFICULTY_CHOICES}
                required={false}
                onChange={onInputChange}
                currentValue={difficulty}
            />
            {children}
        </div>
    );
};

AddKitForm.propTypes = {
    onChange: PropTypes.func.isRequired,
    brand: PropTypes.instanceOf(Brand),
    scale: PropTypes.instanceOf(Scale),
    name: PropTypes.string,
    kitNumber: PropTypes.string,
    difficulty: PropTypes.string,
    children: PropTypes.node,
};

const ModelKitAdd = (props) => {
    const { brand, scale, name, kitNumber, difficulty } = props;
    const {modalBody, modalForm} = useContext(ModalContext);

    const onSubmit = (event) => {
        event.preventDefault();
        const submitData = {
            brand: brand ? brand.id : null,
            scale: scale ? scale.id : null,
            name: name,
            kit_number: kitNumber || "",
            difficulty: difficulty | "",
        };
        console.group("Submit data:");
        console.log(submitData);
        console.groupEnd();
    };

    useEvent("submit", onSubmit, modalForm);

    return ReactDOM.createPortal(
        <AddKitForm {...props} />,
        modalBody
    );
};

export { ModelKitAdd };
