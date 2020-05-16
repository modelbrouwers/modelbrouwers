import React, { useState, useReducer } from 'react';
import PropTypes from 'prop-types';
import { useAsync, useDebounce } from 'react-use';

import { ModelKitConsumer } from '../../data/kits/modelkit';
import { FilterForm } from './FilterForm';
import { KitPreview } from './KitPreview';

const DEBOUNCE = 300;  // debounce in ms

const modelKitConsumer = new ModelKitConsumer();

// TODO: pass selected kit IDs as prop
// TODO: handle toggle changes & allowMultiple yes/no

const searchReducer = (state, {param='', value=null}) => {
    // needs a new object, as the state itself is passed to useDebounce, which appears
    // to be identity checked -> updating just the keys does not
    const newParams = Object.assign({}, state);

    if (!value) {
        delete newParams[param];
        return newParams;
    }

    // otherwise, update the value
    newParams[param] = value;

    // handle pagination - if any param other than page changes, restart at page 1
    if (param !== 'page') {
        delete newParams.page;
    }

    return newParams;
};


const resultsReducer = (state, action) => {
    const { results, forParams: { page } } = action;
    const currentPage = page ?? 1;  // can be undefined
    const allResults = currentPage === 1 ? results : state.results.concat(results);
    return {
        results: allResults,
        hasNext: results.responseData.next != null,
        page: page ?? 1,
    };
};


const ModelKitSelect = ({ label, htmlName, allowMultiple=false, selected=[] }) => {
    // track search parameters state
    const [searchParams, dispatchSearch] = useReducer(searchReducer, {});
    const emptySearch = !Object.keys(searchParams).length;
    const setSearchParam = (param, value) => {
        dispatchSearch({ param, value });
    };

    // track search result state
    const [searchResults, dispatchResults] = useReducer(resultsReducer, {results: [], hasNext: null, page: 1});

    // track which kits are selected
    const [selectedKitIds, setSelectedKitIds] = useState(selected);

    // make an API call whenever the search params change
    const [, cancel] = useDebounce(
        () => {
            if (emptySearch) {
                return;
            }
            modelKitConsumer
                .filter(searchParams)
                .then(resultList => {
                    dispatchResults({results: resultList, forParams: searchParams})
                })
                .catch(console.error);
        },
        DEBOUNCE,
        [searchParams]
    );

    const onKitToggle = (kit, checked) => {
        const isPresent = selectedKitIds.includes(kit.id);
        if (!checked && isPresent) {
            setSelectedKitIds(selectedKitIds.filter(id => id !== kit.id));
        }
        if (checked && !isPresent) {
            selectedKitIds([...selectedKitIds, kit.id]);
        }
    };

    return (
        <React.Fragment>
            <label htmlFor="id_kits"className="control-label col-sm-2"> { label } </label>
            <div className="col-sm-10">
                <div>
                    {/* help text*/}
                    {/* validation errors*/}
                </div>
                <FilterForm setSearchParam={setSearchParam} />
                <div className="kit-suggestions row">

                    <div className="text-center add-kit col-xs-12">
                        {/* TODO: onClick handler */}
                        <a href="#" data-target="#add-kit-modal">
                            <h3>&hellip; of voeg een nieuwe kit toe</h3>
                            <i className="fa fa-plus fa-5x"></i>
                        </a>
                    </div>

                    { searchResults.results.map(
                        kit => <KitPreview
                            key={kit.id}
                            htmlName={htmlName}
                            kit={kit}
                            selected={selectedKitIds.includes(kit.id)}
                            onToggle={onKitToggle}
                        />
                    ) }

                    { searchResults.hasNext ?
                        (
                            <div className="col-xs-12 col-sm-4 col-md-3 col-xl-2 preview center-all">
                                <button className="btn bg-main-blue" type="button" onClick={
                                    () => updateSearchParam('page', searchResults.page + 1)
                                }>
                                    load more
                                </button>
                                <i className="fa fa-pulse fa-spinner fa-4x"></i>
                            </div>
                        )
                        : null
                    }

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

export { ModelKitSelect };
