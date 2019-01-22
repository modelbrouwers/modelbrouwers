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
    changeAmount = amount => {
        const { cartProduct, store } = this.props;
        store.changeAmount(cartProduct.id, amount);
    };

    render() {
        const { cartProduct } = this.props;
        return (
            <div className="controls__row">
                <button
                    className="button button__plus button--blue"
                    onClick={() => this.changeAmount(1)}
                >
                    <i className="fa fa-plus" />
                </button>
                <span className="controls__amount">{cartProduct.amount}</span>

                <button
                    className="button button__minus button--blue"
                    onClick={() => this.changeAmount(-1)}
                >
                    <i className="fa fa-minus" />
                </button>
            </div>
        );
    }
}

AmountControls.propTypes = {};

export default AmountControls;
