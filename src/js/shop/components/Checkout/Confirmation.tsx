import {FormattedMessage} from 'react-intl';

import {useCheckoutContext} from './Context';

const Confirmation: React.FC = () => {
  const {orderDetails} = useCheckoutContext();
  if (orderDetails === null) throw new Error('Cannot show confirmation without order details.');
  const {number: orderNumber, message} = orderDetails;
  return (
    <>
      <h3 style={{marginTop: 0}}>
        <FormattedMessage description="Confirmation title" defaultMessage="Success!" />
      </h3>
      <p>
        <FormattedMessage
          description="Order confirmation generic text"
          defaultMessage="Your order with reference <bold>{orderNumber}</bold> was received! "
          values={{
            orderNumber,
            bold: chunks => <strong>{chunks}</strong>,
          }}
        />
      </p>
      {message && (
        <>
          <h4>
            <FormattedMessage
              description="Confirmation message title"
              defaultMessage="Additional information"
            />
          </h4>
          <p>{message}</p>
        </>
      )}
    </>
  );
};

export default Confirmation;
