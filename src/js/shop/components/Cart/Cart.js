import React, { Component } from "react";
import { observer } from "mobx-react";

@observer
export default class Cart extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        const { store: cart } = this.props;

        return (
            <div className="cart__row">
                <div className="cart__box">
                    <i className="fa fa-shopping-basket cart__icon" />
                    <div className="cart__info">
                        <div className="cart__items">{cart.amount} item(s)</div>
                        <div className="cart__price">&euro; {cart.total}</div>
                    </div>
                </div>
            </div>
        );
    }
}
