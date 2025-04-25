export interface ErrorListProps {
  errors?: string[];
}

const ErrorList: React.FC<ErrorListProps> = ({errors}) => {
  if (!errors || !errors.length) return null;
  return (
    <ul className="errorlist">
      {errors.map((error, index) => (
        <li key={index} className="error">
          {error}
        </li>
      ))}
    </ul>
  );
};

export default ErrorList;
