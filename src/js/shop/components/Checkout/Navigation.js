import React from "react";
import PropTypes from "prop-types";
import classNames from "classnames";
import { HashRouter as Router, Route, NavLink } from "react-router-dom";
import { msg } from "../../../translations/components/Message";
import messages from "./messages";

const tabs = [
    { name: msg(messages.account), url: "/account" },
    { name: msg(messages.address), url: "/address" },
    { name: msg(messages.payment), url: "/payment" },
    { name: msg(messages.confirm), url: "/confirm" }
];
/**
 *
 * Navigation
 *
 */
const Navigation = props => {
    const getLinkClassNames = tab => {
        return classNames("navigation__list-item", {
            "navigation__list-item--active":
                window.location.hash === tab.url.replace("/", "#")
        });
    };

    return (
        <Router hashType="noslash">
            <ul className="navigation__container">
                {tabs.map((tab, i) => {
                    return (
                        <li key={i} className={getLinkClassNames(tab)}>
                            <NavLink className="navigation__link" to={tab.url}>
                                {tab.name}
                            </NavLink>
                        </li>
                    );
                })}
            </ul>
        </Router>
    );
};

Navigation.propTypes = {};

export default Navigation;
