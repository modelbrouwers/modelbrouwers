import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';

import { ModelKitConsumer } from '../../data/kits/modelkit';
import { BrandSelect } from './brand-select';
import { ScaleSelect } from './scale-select';
import { SearchInput } from './search-input';
import { KitPreview } from './kit-preview';

const DEBOUNCE = 300;  // debounce in ms

const modelKitConsumer = new ModelKitConsumer();

// TODO: pass selected kit IDs as prop

const ModelKitSelect = (props) => {
    const {
        label,
        htmlName,
        allowMultiple,
        selected,
    } = props;

    // track search parameters state
    const [searchParams, setSearchParams] = useState({});
    const emptySearch = !Object.keys(searchParams).length;
    // wrap around new object creation to update the search params, as key modification
    // is not observed by React. Also clears the search key if the value is empty.
    const updateSearchParam = (param, value) => {
        const newSearchParams = Object.assign({}, searchParams, {[param]: value});
        if (!value) {
            delete newSearchParams[param];
        }
        setSearchParams(newSearchParams);
    }

    const [searchResults, setSearchResults] = useState([]);

    // make an API call whenever the search params change
    useEffect(() => {
        if (emptySearch) {
            return;
        }
        const tid = window.setTimeout(
            () => {
                modelKitConsumer
                    .filter(searchParams)
                    .then(setSearchResults)
                    .catch(console.error);
            }, DEBOUNCE
        );
        return () => window.clearTimeout(tid);
    }, [searchParams]);

    const onKitToggle = (kit, checked) => {
        console.log(`Kit ${kit.id} checked: ${checked}`);
    };

    return (
        <React.Fragment>
            <label htmlFor="id_kits"className="control-label col-sm-2"> { label } </label>
            <div className="col-sm-10">
                <div>
                    {/* help text*/}
                    {/* validation errors*/}
                </div>
                <FilterForm updateSearchParam={updateSearchParam} />
                <div className="kit-suggestions row">

                    <div className="text-center add-kit col-xs-12">
                        {/* TODO: onClick handler */}
                        <a href="#" data-target="#add-kit-modal">
                            <h3>&hellip; of voeg een nieuwe kit toe</h3>
                            <i className="fa fa-plus fa-5x"></i>
                        </a>
                    </div>

                    { selected.toString() }

                    { searchResults.map(
                        kit => <KitPreview key={kit.id} htmlName={htmlName} kit={kit} onToggle={onKitToggle} />
                    ) }
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


const FilterForm = (props) => {
    const { updateSearchParam } = props;
    return (
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
    );
};

FilterForm.propTypes = {
    updateSearchParam: PropTypes.func.isRequired,
};

export { ModelKitSelect };
