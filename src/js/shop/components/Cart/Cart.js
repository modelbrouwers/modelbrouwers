import React, { Component } from "react";
import { CartConsumer } from "../../../data/albums/cart";
import { Loader } from "../Loader";

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

        this.cartConsumer = new CartConsumer();
    }

    componentDidMount() {
        this.setState({ loading: true });
        this.cartConsumer
            .fetch()
            .then(resp => this.setState({ cart: resp.cart }))
            .catch(err => console.log("Error retrieving cart", err))
            .then(() => this.setState({ loading: false }));
    }

    render() {
        const { cart, loading } = this.state;
        return (
            <div className="cart__row">
                <div className="cart__box">
                    <i className="fa fa-shopping-basket cart__icon" />
                    {loading ? (
                        <Loader />
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
