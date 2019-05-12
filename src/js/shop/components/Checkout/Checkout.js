import React from "react";
import PropTypes from "prop-types";
import { HashRouter as Router, NavLink, Route } from "react-router-dom";
import { msg } from "../../../translations/components/Message";
import messages from "./messages";
import { Account, Address } from "./index";

const tabs = [
    { name: msg(messages.account), url: "/account" },
    { name: msg(messages.address), url: "/address" },
    { name: msg(messages.payment), url: "/payment" },
    { name: msg(messages.confirm), url: "/confirm" }
];

const routes = [
    { path: "/account", component: () => <Account /> },
    { path: "/address", component: () => <Address /> },
    { path: "/payment", component: () => "" },
    { path: "/confirm", component: () => "" }
];

/**
 *
 * Checkout
 *
 */
const Checkout = ({ user }) => {
    const isActive = tab => {
        return window.location.hash === tab.url.replace("/", "#");
    };

    return (
        <div className="checkout">
            <h3 className="checkout__header">{msg(messages.checkout)}</h3>
            <div className="checkout__container">
                <Router hashType="noslash">
                    <ul className="navigation__container">
                        {tabs.map((tab, i) => (
                            <li className="navigation__list-item" key={i}>
                                <NavLink
                                    className="navigation__link"
                                    to={tab.url}
                                    activeClassName="navigation__link--active"
                                    isActive={() => isActive(tab)}
                                >
                                    {tab.name}
                                </NavLink>
                            </li>
                        ))}
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
    user: PropTypes.object
};

export default Checkout;
