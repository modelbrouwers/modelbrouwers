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
    ({ id, store: cart, cartProduct: { amount, product }, canIncrement }) => (
        <div className="controls__row">
            <DecrementButton
                onClick={() => cart.changeAmount(product.id, -1)}
            />
            <span className="controls__amount">{amount}</span>
            <IncrementButton
                onClick={() => cart.changeAmount(product.id, 1)}
                disabled={!canIncrement}
            />
        </div>
    )
);

AmountControls.propTypes = {
    store: PropTypes.object,
    cartProduct: PropTypes.object,
    id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    canIncrement: PropTypes.bool.isRequired,
};

export default AmountControls;
