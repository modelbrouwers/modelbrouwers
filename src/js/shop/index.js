import React from "react";
import ReactDOM from "react-dom";
import { IntlProvider } from "react-intl";

import { CartConsumer } from "../data/shop/cart";
import { TopbarCart, CartProduct, CartDetail } from "./components/Cart";
import { Checkout } from "./components/Checkout";
import { CartStore } from "./store";
import { getIntlProviderProps } from "../i18n";

export default class Page {
    static init() {
        getIntlProviderProps()
            .then((intlProviderProps) => {
                this.intlProviderProps = intlProviderProps;
                this.initRating();
                this.initCart();
            })
            .catch(console.error);
    }

    static initRating() {
        const nodes = document.querySelectorAll(".rating-input__star");
        const activeClass = "rating-input__option--is-active";

        if (nodes && nodes.length) {
            for (let node of nodes) {
                node.addEventListener("click", function (e) {
                    const id = e.target.dataset.id;
                    const el = document.getElementById(id);
                    const activeNodes = document.querySelectorAll(
                        `.${activeClass}`
                    );

                    for (let activeNode of activeNodes) {
                        activeNode.classList.remove(activeClass);
                    }

                    el.parentNode.classList.add(activeClass);
                    el.checked = true;
                });
            }
        }
    }

    static async initCart() {
        const intlProps = this.intlProviderProps;
        const node = document.getElementById("react-cart");
        const detailNode = document.getElementById("react-cart-detail");

        const initCartActions = (cartStore) => {
            const products = document.getElementsByClassName("product-card");

            for (let product of products) {
                const id = product.dataset.product;
                const reactNode = product.querySelector(".react-cart-actions");

                ReactDOM.render(
                    <IntlProvider {...intlProps}>
                        <CartProduct store={cartStore} productId={id} />
                    </IntlProvider>,
                    reactNode
                );
            }
        };

        try {
            this.cartConsumer = new CartConsumer();
            const resp = await this.cartConsumer.fetch();
            const cart = resp.cart;
            let cartStore = new CartStore(cart);
            initCartActions(cartStore);
            this.initCheckout(intlProps);
            ReactDOM.render(
                <IntlProvider {...intlProps}>
                    <TopbarCart store={cartStore} />
                </IntlProvider>,
                node
            );

            if (detailNode) {
                ReactDOM.render(
                    <IntlProvider {...intlProps}>
                        <CartDetail store={cartStore} />
                    </IntlProvider>,
                    detailNode
                );
            }
        } catch (err) {
            console.log("Error retrieving cart", err);
            // TODO render error page/modal/toast
        }
    }

    static initCheckout(intlProps) {
        const node = document.getElementById("react-checkout");

        if (node) {
            ReactDOM.render(
                <IntlProvider {...intlProps}>
                    <Checkout />
                </IntlProvider>,
                node
            );
        }
    }
}
