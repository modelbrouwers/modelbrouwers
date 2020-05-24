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

const AddKitForm = ({ brand = null, scale = null, name = "" }) => {
    const [values, setValues] = useState({
        brand: brand ? brand.id : null,
        scale: scale ? scale.id : null,
        name: name ?? ""
    });
    const onChange = event => {
        const { name, value } = event.target;
        setValues({ ...values, [name]: value });
    };

    return (
        <div className="form-horizontal">
            <FormField htmlId="add-kit-brand" label="brand" required={true}>
                <KitFieldSelect
                    name="brand"
                    consumer={brandConsumer}
                    labelField="name"
                    onChange={onChange}
                    defaultValue={brand}
                />
            </FormField>
            <FormField htmlId="add-kit-scale" label="scale" required={true}>
                <KitFieldSelect
                    name="scale"
                    consumer={scaleConsumer}
                    labelField="__str__"
                    onChange={onChange}
                    defaultValue={scale}
                />
            </FormField>
            <FormField htmlId="add-kit-name" label="name" required={true}>
                <input
                    type="text"
                    name="name"
                    className="form-control"
                    required
                    value={values.name || ""}
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
                    value={values.kit_number || ""}
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
                currentValue={values.difficulty}
            />
            Create params: <code>{JSON.stringify(values)}</code>
        </div>
    );
};

const ModelKitAdd = ({ brand = null, scale = null, name = "" }) => {
    const modalNode = useContext(ModalContext);
    return ReactDOM.createPortal(
        <AddKitForm brand={brand} scale={scale} name={name} />,
        modalNode
    );
};

ModelKitAdd.propTypes = {
    brand: PropTypes.instanceOf(Brand),
    scale: PropTypes.instanceOf(Scale),
    name: PropTypes.string
};

export { ModelKitAdd };
