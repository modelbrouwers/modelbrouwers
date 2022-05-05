import React from "react";
import { Link } from "react-router-dom";
import { FormattedMessage } from "react-intl";

import { SHOP_ROOT } from "../../../constants";

/**
 *
 * Account
 *
 */
const Account = ({ profile }) => {
    // Redirect to next step is user is logged in
    if (profile.user) {
        window.location.href = `${SHOP_ROOT}/checkout/#address`;
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

export default Account;
