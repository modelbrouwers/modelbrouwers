// TODO: handle allowMultiple yes/no
import React, { useReducer } from "react";
import PropTypes from "prop-types";
import { useAsync, useDebounce } from "react-use";
import classNames from "classnames";

import { ModelKitConsumer } from "../../data/kits/modelkit";
import { FilterForm } from "./FilterForm";
import { KitPreview } from "./KitPreview";
import { ModelKitAdd } from "./ModelKitAdd";

const DEBOUNCE = 300; // debounce in ms

const modelKitConsumer = new ModelKitConsumer();

const isEmpty = obj => !Object.keys(obj).length;

const reducer = (allowMultiple, state, action) => {
    switch (action.type) {
        case "UPDATE_SEARCH_PARAM": {
            // update the search param (brand, scale or name)
            // page is handled separately
            const { param, value } = action.payload;
            if (!value) {
                const { [param]: value, ...rest } = state.searchParams;
                return { ...state, searchParams: rest };
            } else {
                const searchParams = { ...state.searchParams, [param]: value };
                return { ...state, searchParams: searchParams };
            }
        }

        case "SET_INITIAL_KITS": {
            // include the pre-selected kits that are _still_ selected
            const kits = action.payload;
            return {
                ...state,
                preSelected: kits.filter(kit =>
                    state.selectedIds.includes(kit.id)
                )
            };
        }

        case "TOGGLE_KIT": {
            // remove kits that get unselected, add kits that get selected
            const { kit, checked } = action.payload;
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

        case "SET_SEARCH_RESULTS": {
            // set the search result if it's page one, or append them if it's a higher page.
            const results = action.payload;
            return {
                ...state,
                searchResults:
                    state.page === 1
                        ? results
                        : [...state.searchResults, ...results],
                hasNext: results.responseData.next !== null
            };
        }

        case "INCREMENT_PAGE":
            return { ...state, page: state.page + 1 };

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
                    type: "SET_INITIAL_KITS",
                    payload: kits
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
                        type: "SET_SEARCH_RESULTS",
                        payload: resultList
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

    // const noResults = !isEmpty(searchParams) && searchResults.length === 0;
    const noResults = true;

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
                            type: "UPDATE_SEARCH_PARAM",
                            payload: {
                                param: param,
                                value: value
                            }
                        })
                    }
                />
                <div
                    className={classNames("row", "kit-suggestions", {
                        "kit-suggestions--no-results": noResults
                    })}
                >
                    <div className="text-center add-kit col-xs-12">
                        <ModelKitAdd />
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
                                dispatch({
                                    type: "TOGGLE_KIT",
                                    payload: { kit, checked }
                                })
                            }
                        />
                    ))}

                    {hasNext ? (
                        <div className="col-xs-12 col-sm-4 col-md-3 col-xl-2 preview center-all">
                            <button
                                className="btn bg-main-blue"
                                type="button"
                                onClick={() =>
                                    dispatch({ type: "INCREMENT_PAGE" })
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
