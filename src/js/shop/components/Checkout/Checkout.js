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
import { Account, Address, Payment, Confirmation } from ".";
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
        case "STATE_FROM_PROPS": {
            const { user, checkoutData } = action.payload;
            const isAuthenticated = Object.keys(user).length > 1;

            // first, process any pre-filled user details (for authenticated users)
            const customer = camelize(user);
            if (isAuthenticated) {
                draft.customer = customer;
                for (const [field, value] of Object.entries(customer.profile)) {
                    draft.deliveryAddress[field] = value;
                }
                draft.deliveryAddress.postalCode = customer.profile.postal;
                if (!draft.deliveryAddress.country) {
                    draft.deliveryAddress.country = "N";
                }
            }

            // next, process the filled out data
            if (checkoutData && Object.keys(checkoutData).length) {
                const {
                    deliveryAddress,
                    invoiceAddress: billingAddress,
                    firstName,
                    lastName,
                    email,
                    phone,
                    paymentMethod,
                    paymentMethodOptions,
                } = camelize(checkoutData);

                if (deliveryAddress) draft.deliveryAddress = deliveryAddress;
                if (billingAddress) draft.billingAddress = billingAddress;
                if (firstName) draft.customer.firstName = firstName;
                if (lastName) draft.customer.lastName = lastName;
                if (email) draft.customer.email = email;
                if (phone) draft.customer.phone = phone;
            }
            break;
        }
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

const checkHasValidationErrors = (validationErrors, errorKey) => {
    const keys = !Array.isArray(errorKey) ? [errorKey] : errorKey;
    if (!validationErrors) return false;
    for (const key of keys) {
        if (!validationErrors[key]) continue;
        const errors = Object.values(validationErrors[key]);
        if (errors.some((errorList) => errorList && errorList.length > 0)) {
            return true;
        }
    }
    return false;
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
    checkoutData,
    orderDetails = null,
    validationErrors,
}) => {
    const location = useLocation();
    const checkoutRoot = useHref("/");

    const isAuthenticated = Object.keys(user).length > 1;
    const [state, dispatch] = useImmerReducer(reducer, initialState);

    useEffect(() => {
        dispatch({
            type: "STATE_FROM_PROPS",
            payload: {
                user,
                checkoutData,
            },
        });
    }, [dispatch, user, checkoutData]);

    useEffect(() => {
        if (location.pathname !== "/") {
            dispatch({ type: "CHECK_ADDRESS_VALIDITY" });
        }
    }, [location, dispatch]);

    const onInputChange = (event) => {
        dispatch({
            type: "FIELD_CHANGED",
            payload: event.target,
        });
        dispatch({ type: "CHECK_ADDRESS_VALIDITY" });
    };

    // re-arrange validation errors to match component structure
    const ERROR_MAP = {
        firstName: "customer.firstName",
        lastName: "customer.lastName",
        email: "customer.email",
        phone: "customer.phone",
    };
    for (const [from, to] of Object.entries(ERROR_MAP)) {
        const errors = get(validationErrors, from);
        if (!errors) continue;
        set(validationErrors, to, errors);
        unset(validationErrors, from);
    }

    const hasAddressValidationErrors = checkHasValidationErrors(
        validationErrors,
        ["customer", "deliveryAddress", "invoiceAddress"]
    );
    const hasPaymentValidationErrors = checkHasValidationErrors(
        validationErrors,
        ["paymentMethod", "paymentMethodOptions", "cart"]
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
                                    checkoutDetails={{
                                        customer: state.customer,
                                        deliveryAddress: state.deliveryAddress,
                                        billingAddress: state.billingAddress,
                                    }}
                                    errors={validationErrors}
                                />
                            }
                        />
                        {/* This is a backend URL - if there are validation errors, it renders
                            the response at this URL. */}
                        <Route
                            path="confirm"
                            element={<Navigate to={firstRouteWithErrors} />}
                        />

                        {/* Success page */}
                        {orderDetails && (
                            <Route
                                path="confirmation"
                                element={
                                    <Confirmation
                                        orderNumber={orderDetails.number}
                                        message={orderDetails.message}
                                    />
                                }
                            />
                        )}
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
                            enabled={!!orderDetails}
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
    checkoutData: PropTypes.object,
    orderDetails: PropTypes.shape({
        number: PropTypes.string.isRequired,
        message: PropTypes.string.isRequired,
    }),
    validationErrors: PropTypes.object,
};

export default Checkout;
