import React from "react";
import { Link } from "react-router-dom";
import { msg } from "../../../translations/components/Message";
import messages from "./messages";

/**
 *
 * Account
 *
 */
const Account = () => {
    return (
        <div className="checkout__inner">
            <div className="checkout__row">
                <Link
                    to="/address"
                    className="button button--blue button--large"
                >
                    {msg(messages.continueNoSignup)}
                </Link>
            </div>

            <div className="checkout__row checkout__row--justified">
                <Link
                    to="/signin"
                    className="button button--blue button--large"
                >
                    {msg(messages.signIn)}
                </Link>

                <Link
                    to="/signup"
                    className="button button--blue button--large"
                >
                    {msg(messages.signUp)}
                </Link>
            </div>
        </div>
    );
};

export default Account;
