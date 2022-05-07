import React from "react";
import PropTypes from "prop-types";
import { Navigate, Link } from "react-router-dom";
import { FormattedMessage } from "react-intl";

import { SHOP_ROOT } from "../../../constants";

/**
 *
 * Account
 *
 */
const Account = ({ isAuthenticated = false }) => {
    if (isAuthenticated) {
        return <Navigate to="/address" />;
    }

    return (
        <div className="checkout__inner">
            <div className="checkout__row">
                <Link
                    to="/address"
                    className="button button--blue button--large"
                >
                    <FormattedMessage
                        description="Checkout with account link"
                        defaultMessage="Continue without signup"
                    />
                </Link>
            </div>

            <div className="checkout__row checkout__row--justified">
                <Link
                    to="/signin"
                    className="button button--blue button--large"
                >
                    <FormattedMessage
                        description="Checkout with login"
                        defaultMessage="Sign in"
                    />
                </Link>

                <Link
                    to="/signup"
                    className="button button--blue button--large"
                >
                    <FormattedMessage
                        description="Checkout with account creation"
                        defaultMessage="Sign up"
                    />
                </Link>
            </div>
        </div>
    );
};

Account.propTypes = {
    isAuthenticated: PropTypes.bool.isRequired,
};

export default Account;
