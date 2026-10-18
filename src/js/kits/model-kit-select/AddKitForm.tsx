import {Form, Formik, useField} from 'formik';

import FormField from '@/components/forms/FormField';
import Radio from '@/components/forms/Radio';
import type {ListBrandData} from '@/data/kits/brand';
import type {ScaleData} from '@/data/kits/scale';

import BoxartUpload from './BoxartUpload';
import CreateBrandSelect from './CreateBrandSelect';
import CreateScaleSelect from './CreateScaleSelect';

interface DiffultyChoice {
  value: '10' | '20' | '30' | '40' | '50';
  label: string;
}

interface FormValues {
  brand: ListBrandData | null;
  scale: ScaleData | null;
  name: string;
  kit_number: string;
  boxartUUID: string;
  difficulty: DiffultyChoice['value'] | '';
}

interface AddKitFormProps {
  onSubmit: (values: FormValues) => void;
  formId: string;
  initialValues?: {
    brand: ListBrandData | null;
    scale: ScaleData | null;
    name: string;
    kit_number: string;
    difficulty: DiffultyChoice['value'] | '';
  };
}

// TODO: translations
const DIFFICULTY_CHOICES: DiffultyChoice[] = [
  {value: '10', label: 'very easy'},
  {value: '20', label: 'easy'},
  {value: '30', label: 'medium'},
  {value: '40', label: 'hard'},
  {value: '50', label: 'very hard'},
];

const AddKitForm: React.FC<AddKitFormProps> = ({formId, onSubmit, initialValues}) => (
  <Formik<FormValues>
    initialValues={{
      brand: initialValues?.brand ?? null,
      scale: initialValues?.scale ?? null,
      name: initialValues?.name ?? '',
      kit_number: initialValues?.kit_number ?? '',
      boxartUUID: '',
      difficulty: initialValues?.difficulty ?? '30',
    }}
    onSubmit={onSubmit}
  >
    {/* ID is necessary to be able to submit it with a button that's not a child of the
        form element */}
    <Form id={formId} className="field-container">
      <FormField htmlId="add-kit-brand" label="Brand" required>
        <CreateBrandSelect name="brand" inputId="add-kit-brand" />
      </FormField>
      <FormField htmlId="add-kit-scale" label="Scale" required>
        <CreateScaleSelect name="scale" inputId="add-kit-scale" />
      </FormField>
      <FormField htmlId="add-kit-name" label="Name" required>
        <NameInput />
      </FormField>
      <FormField htmlId="add-kit-number" label="Kit number" required={false}>
        <KitNumberInput />
      </FormField>
      <FormField htmlId="add-kit-box_image" label="Box image" required={false}>
        <BoxartUpload />
      </FormField>
      <Radio name="difficulty" label="Difficulty" options={DIFFICULTY_CHOICES} appearance="plain" />
    </Form>
  </Formik>
);

// TODO: translations
const NameInput: React.FC = () => {
  const [props] = useField<string>('name');
  return (
    <input
      type="text"
      className="form-control"
      required
      placeholder="kit name"
      id="add-kit-name"
      {...props}
    />
  );
};

// TODO: translations
const KitNumberInput: React.FC = () => {
  const [props] = useField<string>('kit_number');
  return (
    <input
      type="text"
      className="form-control"
      placeholder="kit number"
      id="add-kit-number"
      {...props}
    />
  );
};

export default AddKitForm;
