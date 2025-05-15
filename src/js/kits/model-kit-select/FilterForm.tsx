import PropTypes from 'prop-types';
import Select from 'react-select';
import {useAsync} from 'react-use';

import {type ListBrandData, listBrands} from '@/data/kits/brand';
import {type ScaleData, listScales} from '@/data/kits/scale';

import {SearchInput} from './SearchInput';

const brandOptionGetter = (brand: ListBrandData) => {
  return {
    value: brand.id.toString(),
    label: brand.name,
    option: brand,
  };
};

const scaleOptionGetter = (scale: ScaleData) => {
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
    const [brands, scales] = await Promise.all([listBrands(), listScales()] as const);
    return {brands, scales};
  }, []);

  // throw to nearest error boundary
  if (error) throw error;

  return (
    <div className="row">
      <div className="col-xs-12 col-sm-4">
        <Select<ListBrandData>
          name="brand"
          isLoading={loading}
          options={brands}
          getOptionValue={brand => brand.id.toString()}
          getOptionLabel={brand => brand.name}
          isClearable
          isSearchable
          onChange={selectedOption => onChange({name: 'brand', value: selectedOption ?? null})}
        />
      </div>

      <div className="col-xs-12 col-sm-4">
        <Select<ScaleData>
          name="scale"
          isLoading={loading}
          options={scales}
          getOptionValue={scale => scale.id.toString()}
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
