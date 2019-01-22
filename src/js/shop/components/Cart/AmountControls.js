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

        this.state = {
            amount: props.cartProduct.amount
        };
    }

    updateAmount = e => {
        const { value } = e.target;
        this.setState({ amount: value });
    };

    changeAmount = amount => {
        const { cartProduct, store } = this.props;
        const am = store.changeAmount(cartProduct.id, amount);
        console.log("am", am);
        this.setState({ amount: am });
    };

    render() {
        const { amount } = this.state;
        return (
            <div className="controls__row">
                <input
                    type="text"
                    className="controls__amount"
                    value={amount}
                    onChange={this.updateAmount}
                />
                <button
                    className="button button__plus button--blue"
                    onClick={() => this.changeAmount(1)}
                >
                    <i className="fa fa-plus" />
                </button>
            </div>
        );
    }
}

AmountControls.propTypes = {};

export default AmountControls;
