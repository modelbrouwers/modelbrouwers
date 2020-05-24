import React, { useContext, useState } from "react";
import ReactDOM from "react-dom";
import PropTypes from "prop-types";

import { FormField } from "../../components/forms/FormField";
import { RadioSelect } from "../../components/forms/RadioSelect";

import { Brand } from "../../data/kits/brand";
import { Scale } from "../../data/kits/scale";
import { ModalContext, KitSearchContext } from "./context";
import { BrandAutocomplete } from "./BrandAutocomplete";

// see brouwers.kits.models.KitDifficulties
// TODO: inject this into the DOM and read from the DOM
const DIFFICULTY_CHOICES = [
    { value: 10, display: "very easy" },
    { value: 20, display: "easy" },
    { value: 30, display: "medium" },
    { value: 40, display: "hard" },
    { value: 50, display: "very hard" }
];

const AddKitForm = ({ brand = null, scale = null, name = "" }) => {
    const [values, setValues] = useState({});
    const onChange = event => {
        const { name, value } = event.target;
        setValues({ ...values, [name]: value });
    };

    console.log(values);

    return (
        <div className="form-horizontal">
            <FormField htmlId="add-kit-brand" label="brand" required={true}>
                <BrandAutocomplete brand={brand} onChange={onChange} />
            </FormField>

            <FormField htmlId="add-kit-scale" label="scale" required={true}>
                <input
                    type="text"
                    className="form-control"
                    required
                    defaultValue={scale ? `${scale.__str__}:${scale.id}` : ""}
                />
            </FormField>

            <FormField htmlId="add-kit-name" label="name" required={true}>
                <input
                    type="text"
                    className="form-control"
                    required
                    defaultValue={name}
                    placeholder="kit name"
                />
            </FormField>

            <FormField
                htmlId="add-kit-number"
                label="kit number"
                required={false}
            >
                <input
                    type="text"
                    className="form-control"
                    defaultValue={""}
                    placeholder="kit number"
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
