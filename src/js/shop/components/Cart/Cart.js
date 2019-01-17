import React, { Component } from "react";

export default class Cart extends Component {
    constructor(props) {
        super(props);
        this.state = {
            loading: false,
            cart: {
                total: 0,
                products: []
            }
        };
    }

    render() {
        const { cart, loading } = this.state;
        return (
            <div className="cart__row">
                <div className="cart__box">
                    <i className="fa fa-shopping-basket cart__icon" />
                    {loading ? (
                        <p>Loading...</p>
                    ) : (
                        <div className="cart__info">
                            <div className="cart__items">
                                {cart.products.length} item(s)
                            </div>
                            <div className="cart__price">
                                &euro; {cart.total.toFixed(2)}
                            </div>
                        </div>
                    )}
                </div>
            </div>
        );
    }
}
