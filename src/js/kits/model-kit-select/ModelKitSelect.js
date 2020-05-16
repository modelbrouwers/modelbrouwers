// TODO: handle allowMultiple yes/no
import React, { useState, useReducer } from 'react';
import PropTypes from 'prop-types';
import { useAsync, useDebounce } from 'react-use';

import { ModelKitConsumer } from '../../data/kits/modelkit';
import { FilterForm } from './FilterForm';
import { KitPreview } from './KitPreview';

const DEBOUNCE = 300;  // debounce in ms

const modelKitConsumer = new ModelKitConsumer();

const isEmpty = (obj) => !Object.keys(obj).length;

const reducer = (state, action) => {
    // current state
    const { searchParams, page, selectedIds, preSelected, searchResults, hasNext } = state;

    // create a new state object, defaulting to the existing state
    const newState = Object.assign({}, state);

    const preSelectedIds = preSelected.map(kit => kit.id);

    switch(action.type) {
        case 'searchParam':
            // update the search param (brand, scale or name)
            // page is handled separately
            const { param, value } = action;
            if (!value) {
                delete searchParams[param];
            } else {
                searchParams[param] = value;
            }

            // force creation of a new object
            newState.searchParams = Object.assign({}, searchParams);
            return newState;

        case 'initial':
            // include the pre-selected kits that are _still_ selected
            const { kits } = action;
            newState.preSelected = kits.filter(kit => selectedIds.includes(kit.id));
            return newState;

        case 'kitToggle':
            // remove kits that get unselected, add kits that get selected
            const { kit, checked } = action;
            const isPresent = selectedIds.includes(kit.id);

            if (checked && !isPresent) {
                newState.selectedIds = selectedIds.concat([kit.id]);
            } else if (!checked && isPresent) {
                newState.selectedIds = selectedIds.filter(id => id !== kit.id);
            }

            // remove the kit from the pre selected kits if it gets untoggled - but only
            // if there are search params
            if ( !isEmpty(searchParams) && !checked && preSelectedIds.includes(kit.id) ) {
                newState.preSelected = preSelected.filter(preSelectedKit => preSelectedKit.id !== kit.id);
            }

            return newState;

        case 'search':
            // set the search result if it's page one, or append them if it's a higher page.
            const { results } = action;
            const newSearchResults = page === 1 ? results : searchResults.concat(results);

            newState.searchResults = newSearchResults;
            newState.hasNext = results.responseData.next !== null;
            return newState;

        case 'page':
            newState.page = action.to;
            return newState;
    }
    throw new Error(`Unknown action: ${action.type}`);
};


const ModelKitSelect = ({ label, htmlName, allowMultiple=false, selected=[] }) => {
    // track filter parameters & search results
    const [state, dispatch] = useReducer(
        reducer,
        {
            searchParams: {},
            page: 1,
            selectedIds: selected,  // track PKs of kits that are selected
            preSelected: [],
            searchResults: [],
            hasNext: null,
        }
    );

    const { searchParams, page } = state;

    // load the preview for selected kit IDs
    // this is one-off, so no state dependencies!
    useAsync(() => {
        const promises = state.selectedIds.map(id => modelKitConsumer.read(id));
        return Promise
            .all(promises)
            .then(kits => {
                dispatch({
                    type: 'initial',
                    kits: kits,
                });
            })
            .catch(console.error);
    }, []);

    // make an API call whenever the search params change
    const [, cancel] = useDebounce(
        () => {
            if ( isEmpty(searchParams) ) return;
            modelKitConsumer
                .filter({...searchParams, page: page})
                .then(resultList => {
                    dispatch({
                        type: 'search',
                        results: resultList,
                    });
                })
                .catch(console.error);
        },
        DEBOUNCE,
        [searchParams, page]
    );

    const { preSelected, searchResults } = state;
    const preSelectedIds = preSelected.map(kit => kit.id);
    const searchResultsToRender = searchResults.filter(kit => !preSelectedIds.includes(kit.id))
    const allKits = preSelected.concat(searchResultsToRender);

    return (
        <React.Fragment>
            <label htmlFor="id_kits"className="control-label col-sm-2"> { label } </label>
            <div className="col-sm-10">
                <div>
                    {/* help text*/}
                    {/* validation errors*/}
                </div>
                <FilterForm setSearchParam={ (param, value) => dispatch({type: 'searchParam', param: param, value: value}) } />
                <div className="kit-suggestions row">

                    <div className="text-center add-kit col-xs-12">
                        {/* TODO: onClick handler */}
                        <a href="#" data-target="#add-kit-modal">
                            <h3>&hellip; of voeg een nieuwe kit toe</h3>
                            <i className="fa fa-plus fa-5x"></i>
                        </a>
                    </div>

                    { allKits.map(
                            kit => <KitPreview
                                key={kit.id}
                                htmlName={htmlName}
                                kit={kit}
                                selected={state.selectedIds.includes(kit.id)}
                                onToggle={ (kit, checked) => dispatch({type: 'kitToggle', kit, checked}) }
                            />
                    ) }

                    { state.hasNext ?
                        (
                            <div className="col-xs-12 col-sm-4 col-md-3 col-xl-2 preview center-all">
                                <button className="btn bg-main-blue" type="button" onClick={
                                    () => dispatch({type: 'page', to: state.page + 1})
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
