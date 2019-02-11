import React, { Component } from "react";
import PropTypes from "prop-types";
import { observer } from "mobx-react";
import { DEFAULT_IMAGE } from "../../../constants";
import { AmountControls } from "./index";
import { msg } from "../../../translations/components/Message";
import messages from "./messages";

const headers = [
    msg(messages.image),
    msg(messages.productName),
    msg(messages.model),
    msg(messages.quantity),
    msg(messages.unitPrice),
    msg(messages.totalHeader)
];

/**
 *
 * CartDetail
 *
 */
@observer
class CartDetail extends Component {
    static propTypes = {
        store: PropTypes.object
    };

    constructor(props) {
        super(props);

        this.state = {};
    }

    render() {
        const { store } = this.props;

        return (
            <div className="cart-detail">
                <h2 className="cart-detail__page-header">Shopping Cart</h2>

                <table className="cart-detail__table">
                    <thead className="cart-detail__thead">
                        <tr>
                            {headers.map((header, i) => (
                                <th key={i}>{header}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody className="cart-detail__tbody">
                        {store.products.map((cp, i) => (
                            <tr key={i}>
                                <td>
                                    <img
                                        className="cart-detail__image"
                                        src={cp.product.image || DEFAULT_IMAGE}
                                        alt={cp.product.name}
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
                <div className="cart-totals">
                    <div className="cart-totals__inner">
                        <h4>{msg(messages.cartTotal)}</h4>
                        <div className="cart-totals__row">
                            <span className="cart-totals__text">
                                {msg(messages.subTotal)}
                            </span>
                            <span className="cart-totals__value">N/A</span>
                        </div>
                        <div className="cart-totals__row">
                            <span className="cart-totals__text">
                                {msg(messages.taxes)}
                            </span>
                            <span className="cart-totals__value">N/A</span>
                        </div>
                        <div className="cart-totals__row">
                            <span className="cart-totals__text">
                                {msg(messages.total)}
                            </span>
                            <span className="cart-totals__value">
                                &euro; {store.total}
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

export default CartDetail;
