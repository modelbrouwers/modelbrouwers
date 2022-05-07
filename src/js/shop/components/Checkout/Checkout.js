import React, { useEffect } from "react";
import PropTypes from "prop-types";
import {
    NavLink,
    Routes,
    Route,
    useNavigate,
    useLocation,
} from "react-router-dom";
import { FormattedMessage } from "react-intl";
import classNames from "classnames";

import { Account, Address, Payment } from ".";
import { SHOP_ROOT } from "../../../constants";

const getActiveNavClassNames = ({ isActive }) =>
    classNames("navigation__link", { "navigation__link--active": isActive });

/**
 *
 * Checkout
 *
 */
const Checkout = ({ user, basePath }) => {
    const location = useLocation();
    const navigate = useNavigate();

    const isAuthenticated = Object.keys(user).length > 1;

    // redirect if on the homepage
    useEffect(() => {
        if (location.pathname === "/") {
            const navigateTo = isAuthenticated ? "address" : "account";
            navigate(navigateTo);
            return;
        }
    }, [isAuthenticated, location, navigate]);

    return (
        <div className="nav-wrapper">
            <h2 className="nav-wrapper__title">
                <FormattedMessage
                    description="Checkout header"
                    defaultMessage="Checkout"
                />
            </h2>

            <nav className="nav-wrapper__nav">
                <ul className="navigation">
                    <li className="navigation__item">
                        <NavLink
                            to="account"
                            className={getActiveNavClassNames}
                        >
                            <FormattedMessage
                                description="Tab: account"
                                defaultMessage="Account"
                            />
                        </NavLink>
                    </li>
                    <li className="navigation__item">
                        <NavLink
                            to="address"
                            className={getActiveNavClassNames}
                        >
                            <FormattedMessage
                                description="Tab: address"
                                defaultMessage="Address"
                            />
                        </NavLink>
                    </li>
                    <li className="navigation__item">
                        <NavLink
                            to="payment"
                            className={getActiveNavClassNames}
                        >
                            <FormattedMessage
                                description="Tab: payment"
                                defaultMessage="Payment"
                            />
                        </NavLink>
                    </li>
                    <li className="navigation__item">
                        <NavLink
                            to="confirmation"
                            className={getActiveNavClassNames}
                        >
                            <FormattedMessage
                                description="Tab: confirm"
                                defaultMessage="Confirmation"
                            />
                        </NavLink>
                    </li>
                </ul>
            </nav>

            <div className="nav-wrapper__content">
                <Routes>
                    <Route
                        path="account"
                        element={<Account isAuthenticated={isAuthenticated} />}
                    />
                    <Route path="address" element={<Address user={user} />} />
                </Routes>
            </div>
        </div>
    );
};

Checkout.propTypes = {
    user: PropTypes.shape({
        username: PropTypes.string,
        first_name: PropTypes.string,
        last_name: PropTypes.string,
        email: PropTypes.string,
        phone: PropTypes.string,
        profile: PropTypes.shape({
            street: PropTypes.string.isRequired,
            number: PropTypes.string.isRequired,
            postal: PropTypes.string.isRequired,
            city: PropTypes.string.isRequired,
            country: PropTypes.oneOf(["N", "B", "F", "G"]).isRequired,
        }),
    }),
};

export default Checkout;
