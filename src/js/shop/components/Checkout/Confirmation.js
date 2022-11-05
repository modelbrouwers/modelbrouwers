import React from "react";
import PropTypes from "prop-types";
import { Link } from "react-router-dom";
import { FormattedMessage } from "react-intl";

const Confirmation = ({ orderNumber, message = "" }) => {
    return (
        <>
            <h3 style={{ marginTop: 0 }}>
                <FormattedMessage
                    description="Confirmation title"
                    defaultMessage="Success!"
                />
            </h3>
            <p>
                <FormattedMessage
                    description="Order confirmation generic text"
                    defaultMessage="Your order with reference <bold>{orderNumber}</bold> was received! "
                    values={{
                        orderNumber,
                        bold: (chunks) => <strong>{chunks}</strong>,
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

Confirmation.propTypes = {
    orderNumber: PropTypes.string.isRequired,
    message: PropTypes.string,
};

export default Confirmation;
