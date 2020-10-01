import React from "react";
import PropTypes from "prop-types";

import { BrandConsumer } from "../../data/kits/brand";
import { ScaleConsumer } from "../../data/kits/scale";
import { SearchInput } from "./SearchInput";
import FilterSelect from "./FilterSelect";

const brandConsumer = new BrandConsumer();
const brandOptionGetter = brand => {
    return {
        value: brand.id.toString(),
        label: brand.name,
        option: brand,
    };
};

const scaleConsumer = new ScaleConsumer();
const scaleOptionGetter = scale => {
    return {
        value: scale.id.toString(),
        label: scale.__str__,
        option: scale,
    };
};

const FilterForm = ({ onChange }) => {

    const onSelectChange = (selectedOption, action) => {
        const { name } = action;
        const value = selectedOption ? selectedOption.option : null;
        onChange({name, value});
    };

    const onNameChange = (event) => {
        onChange({
            name: "name",
            value: event.target.value,
        });
    };

    return (
        <div className="row">
            <div className="col-xs-12 col-sm-4">
                <FilterSelect
                    name="brand"
                    consumer={brandConsumer}
                    optionGetter={brandOptionGetter}
                    onChange={onSelectChange}
                />
            </div>

            <div className="col-xs-12 col-sm-4">
                <FilterSelect
                    name="scale"
                    consumer={scaleConsumer}
                    optionGetter={scaleOptionGetter}
                    onChange={onSelectChange}
                />
            </div>

            <div className="col-xs-12 col-sm-4">
                <SearchInput onChange={onNameChange} />
            </div>
        </div>
    );
};

FilterForm.propTypes = {
    onChange: PropTypes.func.isRequired
};

export { FilterForm };
