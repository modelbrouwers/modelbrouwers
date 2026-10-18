import {useField} from 'formik';
import {useState} from 'react';
import CreatableSelect from 'react-select/creatable';
import {useAsync} from 'react-use';

import {type ListBrandData, createBrand, listBrands} from '@/data/kits/brand';

export interface CreateBrandSelectProps {
  name: string;
  inputId?: string;
}

const CreateBrandSelect: React.FC<CreateBrandSelectProps> = ({name, inputId}) => {
  const [props, , {setValue}] = useField<ListBrandData | null>(name);
  const [isLoading, setIsLoading] = useState(false);
  const [brands, setBrands] = useState<ListBrandData[]>([]);
  const {loading, error} = useAsync(async () => setBrands(await listBrands()), []);
  // throw to error boundary
  if (error) throw error;
  if (loading && !isLoading) setIsLoading(true);

  return (
    <CreatableSelect<ListBrandData>
      {...props}
      inputId={inputId}
      isLoading={loading}
      options={brands}
      getOptionValue={brand => brand.id.toString()}
      getOptionLabel={brand => brand.name}
      isClearable
      isSearchable
      getNewOptionData={(inputValue, optionLabel) => ({
        id: inputValue as any as number,
        name: optionLabel as string,
        is_active: true,
      })}
      onCreateOption={async inputValue => {
        setIsLoading(true);
        const brand = await createBrand(inputValue);
        setBrands([...brands, brand]);
        setValue(brand);
        setIsLoading(false);
      }}
      onChange={newValue => {
        setValue(newValue);
      }}
    />
  );
};

export default CreateBrandSelect;
