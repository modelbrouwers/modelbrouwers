import React, { Component } from "react";
import PropTypes from "prop-types";
import { observer } from "mobx-react";

import { DecrementButton, IncrementButton } from "./AmountButtons";

/**
 *
 * AmountControls
 *
 */
@observer
class AmountControls extends Component {
    static propTypes = {
        store: PropTypes.object,
        cartProduct: PropTypes.object,
        id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    };

    constructor(props) {
        super(props);
    }

    changeAmount = (amount) => {
        const { id, store } = this.props;
        store.changeAmount(id, amount);
    };

    render() {
        const { store, cartProduct } = this.props;

        return (
            <div className="controls__row">
                <DecrementButton
                    onClick={() =>
                        store.changeAmount(cartProduct.product.id, -1)
                    }
                />
                <span className="controls__amount">{cartProduct.amount}</span>
                <IncrementButton
                    onClick={() =>
                        store.changeAmount(cartProduct.product.id, 1)
                    }
                />
            </div>
        );
    }
}

export default AmountControls;
