import {useState} from 'react';
import CreatableSelect from 'react-select/creatable';
import {useAsync} from 'react-use';

import {type ScaleData, createScale, listScales, parseScale} from '@/data/kits/scale';

export interface CreateScaleSelectProps {
  onChange: (scale: ScaleData | null) => void;
  value: ScaleData | null;
  inputId?: string;
}

const CreateScaleSelect: React.FC<CreateScaleSelectProps> = ({value, onChange, inputId}) => {
  const [isLoading, setIsLoading] = useState(false);
  const [scales, setScales] = useState<ScaleData[]>([]);
  const {loading, error} = useAsync(async () => setScales(await listScales()), []);
  // throw to error boundary
  if (error) throw error;
  if (loading && !isLoading) setIsLoading(true);

  return (
    <CreatableSelect<ScaleData>
      name="scale"
      inputId={inputId}
      isLoading={loading}
      options={scales}
      value={value}
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
        onChange(scale);
        setIsLoading(false);
      }}
      onChange={onChange}
    />
  );
};

export default CreateScaleSelect;
