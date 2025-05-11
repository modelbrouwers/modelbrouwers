import {FormattedMessage} from 'react-intl';

export interface ErrorMessageProps {
  message?: React.ReactNode;
}

const ErrorMessage: React.FC<ErrorMessageProps> = ({message}) => {
  if (!message) {
    message = (
      <FormattedMessage
        description="General error message"
        defaultMessage="Oops, something went wrong. Please try again later."
      />
    );
  }
  return <div>{message}</div>;
};

export default ErrorMessage;
