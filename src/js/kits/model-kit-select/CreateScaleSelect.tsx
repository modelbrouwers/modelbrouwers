import {useField} from 'formik';
import {useState} from 'react';
import CreatableSelect from 'react-select/creatable';
import {useAsync} from 'react-use';

import {type ScaleData, createScale, listScales, parseScale} from '@/data/kits/scale';

export interface CreateScaleSelectProps {
  name: string;
  inputId?: string;
}

const CreateScaleSelect: React.FC<CreateScaleSelectProps> = ({name, inputId}) => {
  const [props, , {setValue}] = useField<ScaleData | null>(name);
  const [isLoading, setIsLoading] = useState(false);
  const [scales, setScales] = useState<ScaleData[]>([]);
  const {loading, error} = useAsync(async () => setScales(await listScales()), []);
  // throw to error boundary
  if (error) throw error;
  if (loading && !isLoading) setIsLoading(true);

  return (
    <CreatableSelect<ScaleData>
      {...props}
      inputId={inputId}
      isLoading={loading}
      options={scales}
      getOptionValue={scale => scale.id.toString()}
      getOptionLabel={scale => scale.__str__}
      isClearable
      isSearchable
      getNewOptionData={(inputValue, optionLabel) => {
        const numericScale = parseScale(inputValue) || 0;
        return {
          id: inputValue as any as number,
          scale: numericScale,
          __str__: optionLabel as string,
        };
      }}
      onCreateOption={async inputValue => {
        setIsLoading(true);
        const scale = await createScale(inputValue);
        setScales([...scales, scale]);
        setValue(scale);
        setIsLoading(false);
      }}
      onChange={newValue => {
        setValue(newValue);
      }}
    />
  );
};

export default CreateScaleSelect;
