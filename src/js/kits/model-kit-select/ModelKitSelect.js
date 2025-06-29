import classNames from 'classnames';
import PropTypes from 'prop-types';
import React, {useContext, useReducer, useState} from 'react';
import {createPortal} from 'react-dom';
import {FormattedMessage} from 'react-intl';
import {useAsync, useDebounce} from 'react-use';
import {useImmerReducer} from 'use-immer';

import Loader from '@/components/Loader';
import {getModelKit, listModelKits} from '@/data/kits/modelkit';
import AddKitModal from '@/kits/AddKitModal';

import FilterForm from './FilterForm';
import {KitPreviews} from './KitPreview';
import {ModelKitAdd} from './ModelKitAdd';

const DEBOUNCE = 300; // debounce in ms

const FORM_ID = 'add-kit-form';

const isEmpty = obj => !Object.keys(obj).length;

const getInitialState = (selected = []) => {
  return {
    loading: false,
    searchParams: {},
    page: 1,
    selectedIds: selected, // track PKs of kits that are selected
    preSelected: [],
    searchResults: [],
    hasNext: null,
    createKitData: {},
  };
};

const getReducer = allowMultiple => {
  const reducer = (draft, action) => {
    switch (action.type) {
      case 'UPDATE_SEARCH_PARAM': {
        // update the search param (brand, scale or name)
        // page is handled separately
        const {param, value} = action.payload;
        if (!value && draft.searchParams[param]) {
          delete draft.searchParams[param];
        } else if (value) {
          draft.searchParams[param] = value;
        }
        break;
      }

      case 'SET_CREATE_KIT_PARAM': {
        const {param, value} = action.payload;
        if (!value && draft.createKitData) {
          delete draft.createKitData[param];
        } else if (value) {
          draft.createKitData[param] = value;
        }
        break;
      }

      case 'SET_INITIAL_KITS': {
        // include the pre-selected kits that are _still_ selected
        const kits = action.payload;
        draft.preSelected = kits.filter(kit => draft.selectedIds.includes(kit.id));
        break;
      }

      case 'TOGGLE_KIT': {
        // remove kits that get unselected, add kits that get selected
        const {kit, checked} = action.payload;
        const preSelectedIds = draft.preSelected.map(kit => kit.id);

        // remove the kit from the pre selected kits if it gets untoggled - but only
        // if there are search params
        if (!isEmpty(draft.searchParams) && !checked && preSelectedIds.includes(kit.id)) {
          draft.preSelected = draft.preSelected.filter(
            preSelectedKit => preSelectedKit.id !== kit.id,
          );
        }

        // keep track of the selected kit IDs
        if (allowMultiple) {
          const isPresent = draft.selectedIds.includes(kit.id);
          if (checked && !isPresent) {
            draft.selectedIds = draft.selectedIds.concat([kit.id]);
          } else if (!checked && isPresent) {
            draft.selectedIds = draft.selectedIds.filter(id => id !== kit.id);
          }
        } else {
          draft.selectedIds = checked ? [kit.id] : [];
        }
        break;
      }

      case 'SET_SEARCH_RESULTS': {
        // set the search result if it's page one, or append them if it's a higher page.
        const {results, next: nextUrl} = action.payload;
        draft.loading = false;

        if (draft.page === 1) {
          draft.searchResults = results;
        } else {
          draft.searchResults.push(...results);
        }

        draft.hasNext = nextUrl !== null;
        break;
      }

      case 'INCREMENT_PAGE': {
        draft.page++;
        break;
      }

      case 'KIT_CREATED': {
        const kit = action.payload;
        draft.searchResults = [kit, ...draft.searchResults];
        draft.selectedIds = allowMultiple ? [kit.id, ...draft.selectedIds] : [kit.id];
        break;
      }

      case 'SET_LOADING': {
        draft.loading = true;
        break;
      }

      default:
        throw new Error(`Unknown action: ${action.type}`);
    }
  };

  return reducer;
};

const LoadMore = ({show = false, loading = false, onClick, children = 'load more'}) => {
  if (!show) {
    return null;
  }
  return (
    <div className="col-xs-12 col-sm-4 col-md-3 col-xl-2 preview center-all">
      {loading ? (
        <Loader />
      ) : (
        <button className="btn bg-main-blue" type="button" onClick={onClick}>
          {children}
        </button>
      )}
    </div>
  );
};

LoadMore.propTypes = {
  show: PropTypes.bool,
  onClick: PropTypes.func.isRequired,
  children: PropTypes.node,
};

const ModelKitSelect = ({modalNode, label, htmlName, allowMultiple = false, selected = []}) => {
  const [modalOpen, setModalOpen] = useState(false);

  // track filter parameters & search results
  const reducer = getReducer(allowMultiple);
  const initialState = getInitialState(selected);

  const [
    {loading, searchParams, page, selectedIds, preSelected, searchResults, hasNext, createKitData},
    dispatch,
  ] = useImmerReducer(reducer, initialState);

  // load the preview for selected kit IDs
  // this is one-off, so no state dependencies!
  useAsync(async () => {
    const promises = selectedIds.map(getModelKit);
    const kits = await Promise.all(promises);
    dispatch({
      type: 'SET_INITIAL_KITS',
      payload: kits,
    });
  }, []);

  // make an API call whenever the search params change
  // TODO: use the const [_, cancel] = args (on unmount -> cancel)
  useDebounce(
    async () => {
      if (isEmpty(searchParams)) return;
      dispatch({type: 'SET_LOADING'});
      const listResponseData = await listModelKits({...searchParams, page});
      dispatch({type: 'SET_SEARCH_RESULTS', payload: listResponseData});
    },
    DEBOUNCE,
    [searchParams, page],
  );

  const preSelectedIds = preSelected.map(kit => kit.id);
  const searchResultsToRender = searchResults.filter(kit => !preSelectedIds.includes(kit.id));
  const allKits = preSelected.concat(searchResultsToRender);

  /**
   * Handle a change in the search form
   * @param  {String} options.name  Name of the search field
   * @param  {String|Number|Object} options.value Value of the search field
   * @return {Void}               Updates the component state on changes
   */
  const onSearchFieldChange = ({name, value}) => {
    const searchParamValue = name === 'name' ? value : value.id;

    // trigger search
    dispatch({
      type: 'UPDATE_SEARCH_PARAM',
      payload: {
        param: name,
        value: searchParamValue,
      },
    });

    // pre-populate create data
    dispatch({
      type: 'SET_CREATE_KIT_PARAM',
      payload: {
        param: name,
        value: value,
      },
    });
  };

  const onCreateFieldChange = ({name, value}) => {
    dispatch({
      type: 'SET_CREATE_KIT_PARAM',
      payload: {
        param: name,
        value: value,
      },
    });
  };

  const onKitAdded = kit => {
    dispatch({
      type: 'KIT_CREATED',
      payload: kit,
    });
  };

  const noResults = !loading && !isEmpty(searchParams) && searchResults.length === 0;

  const modal = (
    <AddKitModal isOpen={modalOpen} onRequestClose={() => setModalOpen(false)} formId={FORM_ID}>
      <ModelKitAdd
        formId={FORM_ID}
        brand={createKitData.brand}
        scale={createKitData.scale}
        name={createKitData.name}
        kitNumber={createKitData.kit_number}
        difficulty={createKitData.difficulty}
        boxartUUID={createKitData.boxartUUID}
        onChange={onCreateFieldChange}
        onKitAdded={onKitAdded}
      />
    </AddKitModal>
  );

  return (
    <>
      <label htmlFor="id_kits" className="control-label col-sm-2">
        {' '}
        {label}{' '}
      </label>
      <div className="col-sm-10">
        <div>
          {/* help text*/}
          {/* validation errors*/}
        </div>
        <FilterForm onChange={onSearchFieldChange} />

        {loading ? <Loader /> : null}

        <div
          className={classNames('row', 'kit-suggestions', {
            'kit-suggestions--no-results': noResults,
          })}
        >
          {noResults ? (
            <div className="text-center add-kit col-xs-12">
              <a
                href="#"
                onClick={event => {
                  event.preventDefault();
                  setModalOpen(true);
                }}
              >
                <h3>&hellip; of voeg een nieuwe kit toe</h3>
                <i className="fa fa-plus fa-5x" />
              </a>
              {modalNode ? createPortal(modal, modalNode) : modal}
            </div>
          ) : null}

          <KitPreviews
            kits={allKits}
            htmlName={htmlName}
            inputType={allowMultiple ? 'checkbox' : 'radio'}
            selected={selectedIds}
            onToggle={(kit, checked) =>
              dispatch({
                type: 'TOGGLE_KIT',
                payload: {kit, checked},
              })
            }
          />
          <LoadMore
            show={hasNext}
            loading={loading}
            onClick={() => dispatch({type: 'INCREMENT_PAGE'})}
          />
        </div>
      </div>
    </>
  );
};

ModelKitSelect.propTypes = {
  modalNode: PropTypes.instanceOf(HTMLElement),
  label: PropTypes.string.isRequired,
  htmlName: PropTypes.string.isRequired,
  allowMultiple: PropTypes.bool,
  selected: PropTypes.arrayOf(PropTypes.number),
};

export {ModelKitSelect};
