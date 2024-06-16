import { useFormikContext } from "formik";

export interface ErrorListProps {
  name: string;
}

const ErrorList: React.FC<ErrorListProps> = ({ name }) => {
  const { getFieldMeta } = useFormikContext();
  // TODO: deal with *lists* of error messages?
  const meta = getFieldMeta(name);
  if (!meta.touched || !meta.error) return null;

  return (
    <ul className="errorlist">
      <li className="error">{meta.error}</li>
    </ul>
  );
};

export default ErrorList;
