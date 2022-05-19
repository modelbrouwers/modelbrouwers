import React from "react";
import { createRoot } from "react-dom/client";
import { IntlProvider } from "react-intl";
import { BrowserRouter as Router } from "react-router-dom";

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

                createRoot(reactNode).render(
                    <IntlProvider {...intlProps}>
                        <CartProduct store={cartStore} productId={id} />
                    </IntlProvider>
                );
            }
        };

        try {
            this.cartConsumer = new CartConsumer();
            const cart = await this.cartConsumer.fetch();
            let cartStore = new CartStore(cart);
            initCartActions(cartStore);
            this.initCheckout(intlProps, cartStore);
            if (node) {
                createRoot(node).render(
                    <IntlProvider {...intlProps}>
                        <TopbarCart store={cartStore} />
                    </IntlProvider>
                );
            }

            if (detailNode) {
                createRoot(detailNode).render(
                    <IntlProvider {...intlProps}>
                        <CartDetail store={cartStore} />
                    </IntlProvider>
                );
            }
        } catch (err) {
            console.error("Error retrieving cart", err);
            // TODO render error page/modal/toast
        }
    }

    static initCheckout(intlProps, cartStore) {
        const node = document.getElementById("react-checkout");
        if (!node) return;
        const { path: basePath } = node.dataset;
        const root = createRoot(node);

        // read user profile data from DOM, if user is not authenticated, this will be
        // an empty object
        const userProfileScript = document.getElementById("user_profile_data");
        const user = JSON.parse(userProfileScript.innerText);
        // mount and render the checkout component in the DOM
        root.render(
            <IntlProvider {...intlProps}>
                <Router basename={basePath}>
                    <Checkout user={user} cartStore={cartStore} />
                </Router>
            </IntlProvider>
        );
    }
}
