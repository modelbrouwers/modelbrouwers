import React, { Component } from "react";
import { observer } from "mobx-react";
import { CartProductConsumer } from "../../../data/shop/cart";

@observer
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
