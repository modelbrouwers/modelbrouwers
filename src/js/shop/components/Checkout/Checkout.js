import get from "lodash/get";
import unset from "lodash/unset";
import set from "lodash.set";
import React, { useEffect } from "react";
import PropTypes from "prop-types";
import {
    NavLink as RRNavLink,
    Navigate,
    Routes,
    Route,
    useLocation,
    useHref,
} from "react-router-dom";
import { FormattedMessage } from "react-intl";
import classNames from "classnames";
import { useImmerReducer } from "use-immer";

import FAIcon from "../../../components/FAIcon";
import { Account, Address, Payment } from ".";
import { EMPTY_ADDRESS } from "./constants";
import { CheckoutContext } from "./Context";
import { camelize, checkAddressFieldsComplete } from "./utils";

const getActiveNavClassNames = ({ isActive, enabled = false }) =>
    classNames("navigation__link", {
        "navigation__link--active": isActive,
        "navigation__link--enabled": enabled,
    });

const NavLink = ({
    enabled = false,
    className,
    hasErrors = false,
    children,
    ...props
}) => {
    const Container = enabled ? RRNavLink : "span";
    const wrappedClassname = enabled
        ? ({ isActive }) => className({ isActive, enabled })
        : className({ isActive: false, enabled });

    if (hasErrors) {
        children = (
            <span className="nav-link-wrapper">
                <span className="nav-link-wrapper__text">{children}</span>
                <span className="nav-link-wrapper__icon">
                    <FAIcon icon="exclamation-circle" />
                </span>
            </span>
        );
    }

    return (
        <Container {...props} className={wrappedClassname}>
            {children}
        </Container>
    );
};

const initialState = {
    checkoutMode: "withoutAccount",
    customer: {
        firstName: "",
        lastName: "",
        email: "",
        phone: "",
    },
    deliveryAddress: EMPTY_ADDRESS,
    billingAddress: null, // same as delivery address
    addressStepValid: false,
};

const reducer = (draft, action) => {
    switch (action.type) {
        case "FIELD_CHANGED": {
            const { name, value } = action.payload;
            set(draft, name, value);
            break;
        }
        case "CHECK_ADDRESS_VALIDITY": {
            draft.addressStepValid = checkAddressFieldsComplete(
                draft.customer,
                draft.deliveryAddress
            );
            break;
        }
        default: {
            throw new Error(`Unknown action type: ${action.type}`);
        }
    }
};

const checkHasValidationErrors = (validationErrors, key) => {
    if (!validationErrors) return false;
    if (!validationErrors[key]) return false;
    const errors = Object.values(validationErrors[key]);
    return errors.some((errorList) => errorList && errorList.length > 0);
};

/**
 *
 * Checkout
 *
 */
const Checkout = ({
    cartStore,
    user,
    csrftoken,
    confirmPath,
    validationErrors,
}) => {
    const location = useLocation();
    const checkoutRoot = useHref("/");

    const isAuthenticated = Object.keys(user).length > 1;
    const customer = camelize(user);

    const dynamicInitialState = {
        ...initialState,
        checkoutMode: isAuthenticated ? "withAccount" : "withoutAccount",
    };
    if (isAuthenticated) {
        dynamicInitialState.customer = customer;
        dynamicInitialState.deliveryAddress = {
            ...dynamicInitialState.deliveryAddress,
            ...customer.profile,
        };
        dynamicInitialState.deliveryAddress.postalCode =
            dynamicInitialState.deliveryAddress.postal;
        if (dynamicInitialState.deliveryAddress.country == null) {
            dynamicInitialState.deliveryAddress.country = "N";
        }
    }

    const [state, dispatch] = useImmerReducer(reducer, dynamicInitialState);

    // redirect if on the homepage
    useEffect(() => {
        if (location.pathname !== "/") {
            dispatch({ type: "CHECK_ADDRESS_VALIDITY" });
        }
    }, [isAuthenticated, location, dispatch]);

    const onInputChange = (event) => {
        dispatch({
            type: "FIELD_CHANGED",
            payload: event.target,
        });
        dispatch({ type: "CHECK_ADDRESS_VALIDITY" });
    };

    // re-arrange validation errors to match component structure
    const ERROR_MAP = {
        "payment.firstName": "address.firstName",
        "payment.lastName": "address.lastName",
        "payment.email": "address.email",
        "payment.phone": "address.phone",
    };
    for (const [from, to] of Object.entries(ERROR_MAP)) {
        const errors = get(validationErrors, from);
        if (!errors) continue;
        set(validationErrors, to, errors);
        unset(validationErrors, from);
    }

    const hasAddressValidationErrors = checkHasValidationErrors(
        validationErrors,
        "address"
    );
    const hasPaymentValidationErrors = checkHasValidationErrors(
        validationErrors,
        "payment"
    );
    let firstRouteWithErrors = "/";
    if (hasAddressValidationErrors) {
        firstRouteWithErrors = "/address";
    } else if (hasPaymentValidationErrors) {
        firstRouteWithErrors = "/payment";
    }

    return (
        <div className="nav-wrapper">
            <h2 className="nav-wrapper__title">
                <FormattedMessage
                    description="Checkout header"
                    defaultMessage="Checkout"
                />
            </h2>

            <div className="nav-wrapper__content">
                <CheckoutContext.Provider
                    value={{
                        validationErrors,
                        customer: state.customer,
                        deliveryAddress: state.deliveryAddress,
                        billingAddress: state.billingAddress,
                    }}
                >
                    <Routes>
                        <Route
                            path="/"
                            element={
                                <Navigate
                                    to={isAuthenticated ? "address" : "account"}
                                />
                            }
                        />
                        <Route
                            path="account"
                            element={
                                <Account
                                    isAuthenticated={isAuthenticated}
                                    currentLocation={checkoutRoot}
                                />
                            }
                        />
                        <Route
                            path="address"
                            element={
                                <Address
                                    customer={state.customer}
                                    deliveryAddress={state.deliveryAddress}
                                    billingAddress={state.billingAddress}
                                    onChange={onInputChange}
                                    allowSubmit={state.addressStepValid}
                                />
                            }
                        />
                        <Route
                            path="payment"
                            element={
                                <Payment
                                    cartStore={cartStore}
                                    csrftoken={csrftoken}
                                    confirmPath={confirmPath}
                                />
                            }
                        />
                        {/* This is a backend URL - if there are validation errors, it renders
                            the response at this URL. */}
                        <Route
                            path="confirm"
                            element={<Navigate to={firstRouteWithErrors} />}
                        />
                    </Routes>
                </CheckoutContext.Provider>
            </div>

            <nav className="nav-wrapper__nav">
                <ul className="navigation">
                    <li className="navigation__item">
                        <NavLink
                            to="account"
                            className={getActiveNavClassNames}
                            enabled={!isAuthenticated}
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
                            enabled
                            hasErrors={hasAddressValidationErrors}
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
                            enabled={state.addressStepValid}
                            hasErrors={hasPaymentValidationErrors}
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
        </div>
    );
};

Checkout.propTypes = {
    cartStore: PropTypes.object.isRequired,
    csrftoken: PropTypes.string.isRequired,
    confirmPath: PropTypes.string.isRequired,
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
            country: PropTypes.oneOf(["", "N", "B", "F", "G"]),
        }),
    }),
    validationErrors: PropTypes.object,
};

export default Checkout;
