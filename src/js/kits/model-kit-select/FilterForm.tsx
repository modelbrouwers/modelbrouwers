import PropTypes from 'prop-types';
import Select from 'react-select';
import {useAsync} from 'react-use';

import {BrandConsumer} from '../../data/kits/brand';
import {ScaleConsumer} from '../../data/kits/scale';
import {SearchInput} from './SearchInput';

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

interface FilterFormProps {
  onChange: (event: any) => void;
}

const FilterForm: React.FC<FilterFormProps> = ({onChange}) => {
  // pre-load the brands and scales to filter kits on
  const {
    loading,
    value: {brands = [], scales = []} = {},
    error,
  } = useAsync(async () => {
    const [brands, scales] = await Promise.all([brandConsumer.list(), scaleConsumer.list()]);
    return {brands, scales};
  }, []);

  // throw to nearest error boundary
  if (error) throw error;

  return (
    <div className="row">
      <div className="col-xs-12 col-sm-4">
        <Select
          name="brand"
          isLoading={loading}
          options={brands}
          getOptionValue={brand => brand.id}
          getOptionLabel={brand => brand.name}
          isClearable
          isSearchable
          onChange={selectedOption => onChange({name: 'brand', value: selectedOption ?? null})}
        />
      </div>

      <div className="col-xs-12 col-sm-4">
        <Select
          name="scale"
          isLoading={loading}
          options={scales}
          getOptionValue={scale => scale.id}
          getOptionLabel={scale => scale.__str__}
          isClearable
          isSearchable
          onChange={selectedOption => onChange({name: 'scale', value: selectedOption ?? null})}
        />
      </div>

      <div className="col-xs-12 col-sm-4">
        <SearchInput
          onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
            onChange({
              name: 'name',
              value: event.target.value,
            });
          }}
        />
      </div>
    </div>
  );
};

FilterForm.propTypes = {
  onChange: PropTypes.func.isRequired,
};

export {FilterForm, brandOptionGetter, scaleOptionGetter};
