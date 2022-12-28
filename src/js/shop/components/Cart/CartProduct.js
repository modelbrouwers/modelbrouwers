import React from "react";
import PropTypes from "prop-types";
import { observer } from "mobx-react";
import { FormattedMessage } from "react-intl";

import { AmountControls } from "./index";

const CartProduct = observer(({ store: cart, productId, hasStock }) => {
    const cartProduct = cart.findProduct(productId);

    if (!cartProduct || cartProduct.amount <= 0) {
        return (
            <button
                className="button button--blue button__add"
                onClick={() => {
                    cart.addProduct({
                        product: productId,
                        amount: 1,
                    });
                }}
                disabled={!hasStock}
            >
                <FormattedMessage
                    id="shop.cart.product.actions.add"
                    defaultMessage="Add to cart"
                />
            </button>
        );
    }

    return (
        <AmountControls
            store={cart}
            id={productId}
            cartProduct={cartProduct}
            canIncrement={hasStock}
        />
    );
});

CartProduct.propTypes = {
    store: PropTypes.object.isRequired,
    productId: PropTypes.string.isRequired,
    hasStock: PropTypes.bool.isRequired,
};

export default CartProduct;
