import React, { Component } from "react";
import { CartProductConsumer } from "../../../data/albums/cart";

class CartProduct extends Component {
    constructor(props) {
        super(props);
        this.cartProductConsumer = new CartProductConsumer();
    }
    add = () => {
        const { product, cart } = this.props;
        return this.cartProductConsumer
            .addProduct({
                product,
                cart: cart.id,
                amount: 1
            })
            .then(resp => console.log("Product added", resp))
            .catch(err => console.log("Error adding a product", err));
    };
    render() {
        return (
            <button
                className="button button--blue button__add"
                onClick={this.add}
            >
                Add to Cart
            </button>
        );
    }
}

export default CartProduct;
