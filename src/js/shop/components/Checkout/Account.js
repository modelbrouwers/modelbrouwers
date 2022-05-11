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
const Account = ({ isAuthenticated = false, currentLocation = "/" }) => {
    if (isAuthenticated) {
        return <Navigate to="/address" />;
    }

    return (
        <>
            <div className="layout layout--columns">
                <div className="layout__column layout__column--center">
                    <Link
                        to="/address"
                        className="button button--vertical-center button--large button--icon button--blue"
                    >
                        <i className="fa fa-user-secret fa-2x" />
                        <FormattedMessage
                            description="Checkout with account link"
                            defaultMessage="Continue without signup"
                        />
                    </Link>
                </div>

                <div className="layout__separator layout__separator--vertical"></div>

                <div className="layout__column layout__column--center">
                    <div className="layout layout--rows">
                        <div className="layout__row">
                            <a
                                href={`/login/?next=${currentLocation}`}
                                className="button button--blue button--large button--icon button--vertical-center"
                            >
                                <i className="fa fa-sign-in" />
                                <FormattedMessage
                                    description="Checkout with login"
                                    defaultMessage="Sign in"
                                />
                            </a>
                        </div>

                        <div className="layout__separator layout__separator--horizontal">
                            <FormattedMessage
                                description="'Or' (Separator between options)"
                                defaultMessage="or"
                            />
                        </div>

                        <div className="layout__row">
                            <a
                                href={`/register/?next=${currentLocation}&from=checkout`}
                                className="button button--plain button--large button--icon button--vertical-center"
                            >
                                <i className="fa fa-user-plus" />
                                <FormattedMessage
                                    description="Checkout with account creation"
                                    defaultMessage="Sign up"
                                />
                            </a>
                        </div>
                    </div>
                </div>
            </div>

            <div className="message message--info">
                <i className="fa fa-fw fa-info-circle" />
                <FormattedMessage
                    description="Checkout account options description"
                    defaultMessage="Please select how you'd like to continue. No account is required for checkout, but if you do have or create one, we can fill out your details for you (in the future)."
                />
            </div>
        </>
    );
};

Account.propTypes = {
    isAuthenticated: PropTypes.bool.isRequired,
    currentLocation: PropTypes.string.isRequired,
};

export default Account;
