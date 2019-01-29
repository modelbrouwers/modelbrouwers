import React, { Component } from "react";
import { observer } from "mobx-react";
import classNames from "classnames";
import { DEFAULT_IMAGE } from "../../../constants";

@observer
export default class Cart extends Component {
    constructor(props) {
        super(props);

        this.state = { expanded: false };
    }

    expandCart = () => {
        this.setState({ expanded: true });
    };

    collapseCart = () => {
        this.setState({ expanded: false });
    };

    render() {
        const { store: cart } = this.props;
        const { expanded } = this.state;
        const containerClasses = classNames("cart__container", {
            "cart__container--expanded": expanded
        });

        return (
            <div className="cart__row">
                <div
                    className={containerClasses}
                    onMouseOver={this.expandCart}
                    onMouseOut={this.collapseCart}
                >
                    <div className="cart__box">
                        <div className="cart__inner">
                            <i className="fa fa-shopping-basket cart__icon" />
                            <div className="cart__info">
                                <div className="cart__items">
                                    {cart.amount} item(s)
                                </div>
                                <div className="cart__price">
                                    &euro; {cart.total}
                                </div>
                            </div>
                        </div>
                        <div className="cart__actions">
                            <button className="button button--blue">
                                View cart
                            </button>
                            <button className="button button--blue">
                                Checkout
                            </button>
                        </div>
                    </div>
                    <ul className="cart__products">
                        {cart.products.map((product, i) => (
                            <li className="cart-product" key={i}>
                                <div className="cart-product__image">
                                    <img
                                        src={
                                            product.product.image ||
                                            DEFAULT_IMAGE
                                        }
                                        alt={product.name}
                                    />
                                </div>
                                <p className="cart-product__name">
                                    {product.product.name}
                                </p>
                                <div className="cart-product__amount">
                                    {product.amount}
                                </div>
                                <div className="cart-product__price">
                                    &euro; {product.product.price}
                                </div>
                                <div
                                    className="cart-product__remove"
                                    onClick={() =>
                                        cart.removeProduct(product.id)
                                    }
                                >
                                    <i className="fa fa-close" />
                                </div>
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
        );
    }
}
