import React from "react";
import PropTypes from "prop-types";
import { HashRouter as Router, NavLink, Route } from "react-router-dom";
import { FormattedMessage } from "react-intl";
import { Account, Address, Payment } from "./index";
import { SHOP_ROOT } from "../../../constants";

/**
 *
 * Checkout
 *
 */
const Checkout = ({ profile }) => {
    const tabs = [
        {
            name: (
                <FormattedMessage
                    description="Tab: account"
                    defaultMessage="Account"
                />
            ),
            url: "/account",
            hidden: profile.user,
        },
        {
            name: (
                <FormattedMessage
                    description="Tab: address"
                    defaultMessage="Address"
                />
            ),
            url: "/address",
        },
        {
            name: (
                <FormattedMessage
                    description="Tab: payment"
                    defaultMessage="Payment"
                />
            ),
            url: "/payment",
        },
        {
            name: (
                <FormattedMessage
                    description="Tab: confirm"
                    defaultMessage="Confirmation"
                />
            ),
            url: "/confirm",
        },
    ];

    const routes = [
        {
            path: "/account",
            component: (props) => <Account {...props} profile={profile} />,
            hidden: profile.user,
        },
        {
            path: "/address",
            component: (props) => <Address {...props} profile={profile} />,
        },
        {
            path: "/payment",
            component: (props) => <Payment {...props} profile={profile} />,
        },
        { path: "/confirm", component: () => "" },
    ];

    const isActive = (tab) => {
        return window.location.hash === tab.url.replace("/", "#");
    };

    if (window.location.pathname === `${SHOP_ROOT}/checkout/`) {
        window.location.href = `${SHOP_ROOT}/checkout/#account`;
    }

    return (
        <div className="checkout">
            <h2 className="checkout__header">
                <FormattedMessage
                    description="Checkout header"
                    defaultMessage="Checkout"
                />
            </h2>
            <div className="checkout__container">
                <Router hashType="noslash">
                    <ul className="navigation__container">
                        {tabs.map(
                            (tab, i) =>
                                !tab.hidden && (
                                    <li
                                        className="navigation__list-item"
                                        key={i}
                                    >
                                        <NavLink
                                            className="navigation__link"
                                            to={tab.url}
                                            activeClassName="navigation__link--active"
                                            isActive={() => isActive(tab)}
                                        >
                                            {tab.name}
                                        </NavLink>
                                    </li>
                                )
                        )}
                    </ul>
                    {routes.map((route, i) => (
                        <Route
                            key={i}
                            path={route.path}
                            exact={route.exact}
                            component={route.component}
                        />
                    ))}
                </Router>
            </div>
        </div>
    );
};

Checkout.propTypes = {
    user: PropTypes.object,
};

export default Checkout;
