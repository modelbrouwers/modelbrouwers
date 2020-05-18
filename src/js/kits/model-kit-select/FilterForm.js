import React from "react";
import PropTypes from "prop-types";

import { BrandConsumer } from "../../data/kits/brand";
import { ScaleConsumer } from "../../data/kits/scale";
import { SearchInput } from "./SearchInput";
import { AsyncSelect } from "./AsyncSelect";

const brandConsumer = new BrandConsumer();
const brandOptionGetter = brand => {
    return {
        value: brand.id,
        label: brand.name
    };
};

const scaleConsumer = new ScaleConsumer();
const scaleOptionGetter = scale => {
    return {
        value: scale.id,
        label: scale.__str__
    };
};

const FilterForm = ({ setSearchParam }) => {
    return (
        <div className="row">
            <div className="col-xs-12 col-sm-4">
                <AsyncSelect
                    consumer={brandConsumer}
                    optionGetter={brandOptionGetter}
                    onChange={setSearchParam.bind(this, "brand")}
                />
            </div>

            <div className="col-xs-12 col-sm-4">
                <AsyncSelect
                    consumer={scaleConsumer}
                    optionGetter={scaleOptionGetter}
                    onChange={setSearchParam.bind(this, "scale")}
                />
            </div>

            <div className="col-xs-12 col-sm-4">
                <SearchInput onChange={setSearchParam.bind(this, "name")} />
            </div>
        </div>
    );
};

FilterForm.propTypes = {
    setSearchParam: PropTypes.func.isRequired
};

export { FilterForm };
