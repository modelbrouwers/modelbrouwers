import React, { useState } from 'react';
import PropTypes from 'prop-types';

import { BrandSelect } from './brand-select';
import { ScaleSelect } from './scale-select';
import { SearchInput } from './search-input';

// TODO: pass selected kit IDs as prop
// for TODOs/missing aspects -> see horizontal.form for the markup

const ModelKitSelect = (props) => {
    const {
        label,
        htmlName,
        allowMultiple,
        selected,
    } = props;

    const [searchParams, setSearchParams] = useState({});

    const updateSearchParam = (param, value) => {
        const newSearchParams = Object.assign({}, searchParams, {[param]: value});
        setSearchParams(newSearchParams);
    }

    return (
        <React.Fragment>
            <label htmlFor="id_kits"className="control-label col-sm-2"> { label } </label>

            <div className="col-sm-10">
                <div>
                    {/* help text*/}
                    {/* validation errors*/}
                </div>

                <div className="row">
                    <div className="col-xs-12 col-sm-4">
                        <BrandSelect onChange={ (pk) => updateSearchParam('brand', pk) } />
                    </div>

                    <div className="col-xs-12 col-sm-4">
                        <ScaleSelect onChange={ (pk) => updateSearchParam('scale', pk) } />
                    </div>

                    <div className="col-xs-12 col-sm-4">
                        <SearchInput onChange={ (query) => updateSearchParam('name', query) } />
                    </div>
                </div>

                <div className="kit-suggestions row">

                    <div className="text-center add-kit col-xs-12">
                        {/* TODO: onClick handler */}
                        <a href="#" data-target="#add-kit-modal">
                            <h3>&hellip; of voeg een nieuwe kit toe</h3>
                            <i className="fa fa-plus fa-5x"></i>
                        </a>
                    </div>

                    { selected.toString() }
                    { JSON.stringify(searchParams) }
                </div>
            </div>
        </React.Fragment>
    );
};

ModelKitSelect.propTypes = {
    label: PropTypes.string.isRequired,
    htmlName: PropTypes.string.isRequired,
    allowMultiple: PropTypes.bool,
    selected: PropTypes.arrayOf(PropTypes.number),
};

ModelKitSelect.defaultProps = {
    allowMultiple: false,
    selected: [],
};


export { ModelKitSelect };
