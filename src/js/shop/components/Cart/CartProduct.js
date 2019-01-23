import React, { Component } from "react";
import { observer } from "mobx-react";
import { CartProductConsumer } from "../../../data/shop/cart";
import { AmountControls } from "./index";

@observer
class CartProduct extends Component {
    constructor(props) {
        super(props);
        this.cartProductConsumer = new CartProductConsumer();
    }
    add = () => {
        const { productId, cart, store } = this.props;
        const cartProduct = store.findProduct(productId);
        return this.cartProductConsumer
            .addProduct({
                product: productId,
                cart: cart.id,
                amount: 1
            })
            .then(resp => console.log("added prod", resp))
            .catch(err => console.log("Error adding product", err));
    };

    render() {
        const { productId, store } = this.props;
        const cartProduct = store.findProduct(productId);

        return cartProduct && cartProduct.amount > 0 ? (
            <AmountControls id={productId} store={store} />
        ) : (
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
