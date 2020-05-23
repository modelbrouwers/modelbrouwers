import React from "react";
import PropTypes from "prop-types";

import { BrandConsumer } from "../../data/kits/brand";
import { ScaleConsumer } from "../../data/kits/scale";
import { SearchInput } from "./SearchInput";
import { AsyncSelect } from "./AsyncSelect";

const brandConsumer = new BrandConsumer();
const brandOptionGetter = brand => {
    return {
        value: brand.id.toString(),
        label: brand.name,
        option: brand
    };
};

const scaleConsumer = new ScaleConsumer();
const scaleOptionGetter = scale => {
    return {
        value: scale.id.toString(),
        label: scale.__str__,
        option: scale
    };
};

const FilterForm = ({ setSearchParam }) => {
    return (
        <div className="row">
            <div className="col-xs-12 col-sm-4">
                <AsyncSelect
                    consumer={brandConsumer}
                    optionGetter={brandOptionGetter}
                    onChange={setSearchParam.bind(null, "brand")}
                />
            </div>

            <div className="col-xs-12 col-sm-4">
                <AsyncSelect
                    consumer={scaleConsumer}
                    optionGetter={scaleOptionGetter}
                    onChange={setSearchParam.bind(null, "scale")}
                />
            </div>

            <div className="col-xs-12 col-sm-4">
                <SearchInput onChange={setSearchParam.bind(null, "name")} />
            </div>
        </div>
    );
};

FilterForm.propTypes = {
    setSearchParam: PropTypes.func.isRequired
};

export { FilterForm };
