import React, { Component } from "react";
import PropTypes from "prop-types";
import { observer } from "mobx-react";

import { DecrementButton, IncrementButton } from "./AmountButtons";

/**
 *
 * AmountControls
 *
 */
const AmountControls = observer(
    ({ id, store: cart, cartProduct: { amount, product } }) => (
        <div className="controls__row">
            <DecrementButton
                onClick={() => cart.changeAmount(product.id, -1)}
            />
            <span className="controls__amount">{amount}</span>
            <IncrementButton onClick={() => cart.changeAmount(product.id, 1)} />
        </div>
    )
);

AmountControls.propTypes = {
    store: PropTypes.object,
    cartProduct: PropTypes.object,
    id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
};

export default AmountControls;
