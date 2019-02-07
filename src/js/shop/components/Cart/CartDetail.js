import React, { Component } from "react";
import PropTypes from "prop-types";
import { observer } from "mobx-react";
import { DEFAULT_IMAGE } from "../../../constants";
import { AmountControls } from "./index";

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
                            <th>Image</th>
                            <th>Product Name</th>
                            <th>Model</th>
                            <th>Quantity</th>
                            <th>Unit Price</th>
                            <th>Total</th>
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
            </div>
        );
    }
}

export default CartDetail;
