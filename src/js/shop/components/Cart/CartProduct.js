import React, { Component } from "react";
import { observer } from "mobx-react";
import { AmountControls } from "./index";

@observer
class CartProduct extends Component {
    constructor(props) {
        super(props);
    }

    add = () => {
        const { productId, store } = this.props;
        return store.addProduct({
            product: productId,
            cart: store.id,
            amount: 1
        });
    };

    render() {
        const { productId, store } = this.props;
        const cartProduct = store.findProduct(productId);

        return cartProduct && cartProduct.amount > 0 ? (
            <AmountControls
                store={store}
                id={productId}
                cartProduct={cartProduct}
            />
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
