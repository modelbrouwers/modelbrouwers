// TODO: handle allowMultiple yes/no
import React, { useReducer } from "react";
import PropTypes from "prop-types";
import { useAsync, useDebounce } from "react-use";

import { ModelKitConsumer } from "../../data/kits/modelkit";
import { FilterForm } from "./FilterForm";
import { KitPreview } from "./KitPreview";

const DEBOUNCE = 300; // debounce in ms

const modelKitConsumer = new ModelKitConsumer();

const isEmpty = obj => !Object.keys(obj).length;

const reducer = (allowMultiple, state, action) => {
    switch (action.type) {
        case "searchParam": {
            // update the search param (brand, scale or name)
            // page is handled separately
            const { param, value } = action;
            if (!value) {
                const { [param]: value, ...rest } = state.searchParams;
                return { ...state, searchParams: rest };
            } else {
                const searchParams = { ...state.searchParams, [param]: value };
                return { ...state, searchParams: searchParams };
            }
        }

        case "initial": {
            // include the pre-selected kits that are _still_ selected
            const { kits } = action;
            return {
                ...state,
                preSelected: kits.filter(kit =>
                    state.selectedIds.includes(kit.id)
                )
            };
        }

        case "kitToggle": {
            // remove kits that get unselected, add kits that get selected
            const { kit, checked } = action;
            let preSelected = state.preSelected;
            const preSelectedIds = preSelected.map(kit => kit.id);

            // remove the kit from the pre selected kits if it gets untoggled - but only
            // if there are search params
            if (
                !isEmpty(state.searchParams) &&
                !checked &&
                preSelectedIds.includes(kit.id)
            ) {
                preSelected = preSelected.filter(
                    preSelectedKit => preSelectedKit.id !== kit.id
                );
            }

            // keep track of the selected kit IDs
            if (allowMultiple) {
                const isPresent = state.selectedIds.includes(kit.id);
                if (checked && !isPresent) {
                    return {
                        ...state,
                        preSelected: preSelected,
                        selectedIds: state.selectedIds.concat([kit.id])
                    };
                } else if (!checked && isPresent) {
                    return {
                        ...state,
                        preSelected: preSelected,
                        selectedIds: state.selectedIds.filter(
                            id => id !== kit.id
                        )
                    };
                }
                // can't happen, but better safe than sorry?
                return state;
            } else {
                return {
                    ...state,
                    preSelected: preSelected,
                    selectedIds: checked ? [kit.id] : []
                };
            }
        }

        case "search": {
            // set the search result if it's page one, or append them if it's a higher page.
            const { results } = action;
            return {
                ...state,
                searchResults:
                    state.page === 1
                        ? results
                        : [...state.searchResults, ...results],
                hasNext: results.responseData.next !== null
            };
        }

        case "page":
            return { ...state, page: action.to };

        default:
            throw new Error(`Unknown action: ${action.type}`);
    }
};

const ModelKitSelect = ({
    label,
    htmlName,
    allowMultiple = false,
    selected = []
}) => {
    // track filter parameters & search results
    const [
        {
            searchParams,
            page,
            selectedIds,
            preSelected,
            searchResults,
            hasNext
        },
        dispatch
    ] = useReducer(reducer.bind(null, allowMultiple), {
        searchParams: {},
        page: 1,
        selectedIds: selected, // track PKs of kits that are selected
        preSelected: [],
        searchResults: [],
        hasNext: null
    });

    // load the preview for selected kit IDs
    // this is one-off, so no state dependencies!
    useAsync(() => {
        const promises = selectedIds.map(id => modelKitConsumer.read(id));
        return Promise.all(promises)
            .then(kits => {
                dispatch({
                    type: "initial",
                    kits: kits
                });
            })
            .catch(console.error);
    }, []);

    // make an API call whenever the search params change
    // TODO: use the const [_, cancel] = args (on unmount -> cancel)
    useDebounce(
        () => {
            if (isEmpty(searchParams)) return;
            modelKitConsumer
                .filter({ ...searchParams, page: page })
                .then(resultList => {
                    dispatch({
                        type: "search",
                        results: resultList
                    });
                })
                .catch(console.error);
        },
        DEBOUNCE,
        [searchParams, page]
    );

    const preSelectedIds = preSelected.map(kit => kit.id);
    const searchResultsToRender = searchResults.filter(
        kit => !preSelectedIds.includes(kit.id)
    );
    const allKits = preSelected.concat(searchResultsToRender);

    return (
        <React.Fragment>
            <label htmlFor="id_kits" className="control-label col-sm-2">
                {" "}
                {label}{" "}
            </label>
            <div className="col-sm-10">
                <div>
                    {/* help text*/}
                    {/* validation errors*/}
                </div>
                <FilterForm
                    setSearchParam={(param, value) =>
                        dispatch({
                            type: "searchParam",
                            param: param,
                            value: value
                        })
                    }
                />
                <div className="kit-suggestions row">
                    <div className="text-center add-kit col-xs-12">
                        {/* TODO: onClick handler */}
                        <a href="#" data-target="#add-kit-modal">
                            <h3>&hellip; of voeg een nieuwe kit toe</h3>
                            <i className="fa fa-plus fa-5x" />
                        </a>
                    </div>

                    {allKits.map(kit => (
                        <KitPreview
                            key={kit.id}
                            htmlName={htmlName}
                            inputType={allowMultiple ? "checkbox" : "radio"}
                            kit={kit}
                            selected={selectedIds.includes(kit.id)}
                            onToggle={(kit, checked) =>
                                dispatch({ type: "kitToggle", kit, checked })
                            }
                        />
                    ))}

                    {hasNext ? (
                        <div className="col-xs-12 col-sm-4 col-md-3 col-xl-2 preview center-all">
                            <button
                                className="btn bg-main-blue"
                                type="button"
                                onClick={() =>
                                    dispatch({
                                        type: "page",
                                        to: page + 1
                                    })
                                }
                            >
                                load more
                            </button>
                            <i className="fa fa-pulse fa-spinner fa-4x" />
                        </div>
                    ) : null}
                </div>
            </div>
        </React.Fragment>
    );
};

ModelKitSelect.propTypes = {
    label: PropTypes.string.isRequired,
    htmlName: PropTypes.string.isRequired,
    allowMultiple: PropTypes.bool,
    selected: PropTypes.arrayOf(PropTypes.number)
};

export { ModelKitSelect };
