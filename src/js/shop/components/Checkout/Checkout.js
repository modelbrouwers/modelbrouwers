import React, { useEffect } from "react";
import PropTypes from "prop-types";
import { NavLink, useNavigate, useLocation } from "react-router-dom";
import { FormattedMessage } from "react-intl";
import classNames from "classnames";

import { Account, Address, Payment } from "./index";
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

    // redirect if on the homepage
    useEffect(() => {
        const isAuthenticated = Object.keys(user).length > 1;

        if (location.pathname === "/") {
            const navigateTo = isAuthenticated ? "address" : "account";
            navigate(navigateTo);
            return;
        }
    }, [user, location, navigate]);

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

            <div className="nav-wrapper__content">{location.pathname}</div>
        </div>
    );

    // const routes = [
    //     {
    //         path: "/account",
    //         component: (props) => <Account {...props} profile={profile} />,
    //         hidden: profile.user,
    //     },
    //     {
    //         path: "/address",
    //         component: (props) => <Address {...props} profile={profile} />,
    //     },
    //     {
    //         path: "/payment",
    //         component: (props) => <Payment {...props} profile={profile} />,
    //     },
    //     { path: "/confirm", component: () => "" },
    // ];
    // const isActive = (tab) => {
    //     return window.location.hash === tab.url.replace("/", "#");
    // };
    // if (window.location.pathname === `${SHOP_ROOT}/checkout/`) {
    //     window.location.href = `${SHOP_ROOT}/checkout/#account`;
    // }
    // return (
    //     <div className="checkout">
    //         <h2 className="checkout__header">
    //             <FormattedMessage
    //                 description="Checkout header"
    //                 defaultMessage="Checkout"
    //             />
    //         </h2>
    //         <div className="checkout__container">
    //             <Router hashType="noslash">
    //                 <ul className="navigation__container">
    //                     {tabs.map(
    //                         (tab, i) =>
    //                             !tab.hidden && (
    //                                 <li
    //                                     className="navigation__list-item"
    //                                     key={i}
    //                                 >
    //                                     <NavLink
    //                                         className="navigation__link"
    //                                         to={tab.url}
    //                                         activeClassName="navigation__link--active"
    //                                         isActive={() => isActive(tab)}
    //                                     >
    //                                         {tab.name}
    //                                     </NavLink>
    //                                 </li>
    //                             )
    //                     )}
    //                 </ul>
    //                 {routes.map((route, i) => (
    //                     <Route
    //                         key={i}
    //                         path={route.path}
    //                         exact={route.exact}
    //                         component={route.component}
    //                     />
    //                 ))}
    //             </Router>
    //         </div>
    //     </div>
    // );
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
