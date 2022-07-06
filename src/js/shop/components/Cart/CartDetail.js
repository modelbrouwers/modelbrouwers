import React, { Component } from "react";
import PropTypes from "prop-types";
import { observer } from "mobx-react";
import { useIntl, FormattedMessage } from "react-intl";

import { DEFAULT_IMAGE } from "../../../constants";
import { AmountControls } from "./index";
import messages from "./messages";
import ProductImage from "./ProductImage";

const headers = [
    messages.image,
    messages.productName,
    messages.model,
    messages.quantity,
    messages.unitPrice,
    messages.totalHeader,
];

/**
 *
 * CartDetail
 *
 */
const CartDetail = observer(({ store, checkoutPath, indexPath }) => {
    const intl = useIntl();
    return (
        <div className="cart-detail">
            <h2 className="cart-detail__page-header">
                <FormattedMessage
                    description="Shopping cart title"
                    defaultMessage="Shopping cart"
                />
            </h2>

            <table className="cart-detail__table">
                <thead className="cart-detail__thead">
                    <tr>
                        {headers.map((header, i) => (
                            <th key={i}>{intl.formatMessage(header)}</th>
                        ))}
                    </tr>
                </thead>
                <tbody className="cart-detail__tbody">
                    {store.products.map((cp, i) => (
                        <tr key={cp.id}>
                            <td>
                                <ProductImage
                                    product={cp.product}
                                    className="cart-detail__image"
                                />
                            </td>
                            <td>
                                <a href="#" className="cart-detail__name">
                                    {cp.product.name}
                                </a>
                            </td>
                            <td>
                                <p className="cart-detail__model">
                                    {cp.product.model_name}
                                </p>
                            </td>
                            <td className="cart-detail__quantity">
                                <AmountControls
                                    store={store}
                                    cartProduct={cp}
                                    id={cp.product.id}
                                />
                            </td>
                            <td>
                                <p className="cart-detail__unit-price">
                                    &euro; {cp.product.price}
                                </p>
                            </td>
                            <td>
                                <p className="cart-detail__product-total">
                                    &euro; {cp.totalStr}
                                </p>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>

            {/*TODO: Calculate sub-total and taxes*/}
            <div className="cart-detail__row">
                <div className="cart-detail__totals">
                    <div className="cart-detail__inner">
                        <h4>
                            <FormattedMessage
                                id="shop.cart.detail.title.cart.total"
                                defaultMessage="Cart total"
                            />
                        </h4>
                        <div className="cart-detail__info-row">
                            <span className="cart-detail__text">
                                <FormattedMessage
                                    id="shop.cart.detail.cart.subtotal"
                                    defaultMessage="Sub-total"
                                />
                            </span>
                            <span className="cart-detail__value">N/A</span>
                        </div>
                        <div className="cart-detail__info-row">
                            <span className="cart-detail__text">
                                <FormattedMessage
                                    id="shop.cart.detail.cart.taxes"
                                    defaultMessage="Taxes"
                                />
                            </span>
                            <span className="cart-detail__value">N/A</span>
                        </div>
                        <div className="cart-detail__info-row">
                            <span className="cart-detail__text">
                                <FormattedMessage
                                    id="shop.cart.detail.cart.total"
                                    defaultMessage="Total"
                                />
                            </span>
                            <span className="cart-detail__value">
                                &euro; {store.total}
                            </span>
                        </div>
                    </div>

                    <div className="cart-detail__action-row">
                        <a href={indexPath} className="button button--blue">
                            <FormattedMessage
                                description="Button back to webshop homepage"
                                defaultMessage="Continue shopping"
                            />
                        </a>
                        <a href={checkoutPath} className="button button--blue">
                            <FormattedMessage
                                description="Button to webshop checkout"
                                defaultMessage="Checkout"
                            />
                        </a>
                    </div>
                </div>
            </div>
        </div>
    );
});

CartDetail.propTypes = {
    store: PropTypes.object,
    checkoutPath: PropTypes.string.isRequired,
    indexPath: PropTypes.string.isRequired,
};

export default CartDetail;
