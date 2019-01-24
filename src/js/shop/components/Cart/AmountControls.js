import React, { Component } from "react";
import PropTypes from "prop-types";
import { observer } from "mobx-react";

/**
 *
 * AmountControls
 *
 */
@observer
class AmountControls extends Component {
    constructor(props) {
        super(props);
    }

    changeAmount = amount => {
        const { id, store } = this.props;
        store.changeAmount(id, amount);
    };

    render() {
        const { cartProduct, store } = this.props;
        // const cartProduct = store.findProduct(id);
        return (
            <div className="controls__row">
                <button
                    className="button button__plus button--blue"
                    onClick={() => cartProduct.increaseAmount(1)}
                >
                    <i className="fa fa-plus" />
                </button>
                <span className="controls__amount">{cartProduct.amount}</span>

                <button
                    className="button button__minus button--blue"
                    onClick={() => cartProduct.decreaseAmount(1)}
                >
                    <i className="fa fa-minus" />
                </button>
            </div>
        );
    }
}

AmountControls.propTypes = {};

export default AmountControls;
