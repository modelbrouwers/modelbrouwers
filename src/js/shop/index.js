import React from "react";
import { createRoot } from "react-dom/client";
import { IntlProvider } from "react-intl";

import { CartConsumer } from "../data/shop/cart";
import { TopbarCart, CartProduct, CartDetail } from "./components/Cart";
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

    static initCart() {
        const node = document.getElementById("react-cart");
        const detailNode = document.getElementById("react-cart-detail");
        if (node) {
            this.cartConsumer = new CartConsumer();
            this.cartConsumer
                .fetch()
                .then(({ cart }) => {
                    let cartStore = new CartStore(cart);
                    initCartActions(cartStore);
                    createRoot(node).render(
                        <IntlProvider {...this.intlProviderProps}>
                            <TopbarCart store={cartStore} />
                        </IntlProvider>
                    );

                    if (detailNode) {
                        createRoot(detailNode).render(
                            <IntlProvider {...this.intlProviderProps}>
                                <CartDetail store={cartStore} />
                            </IntlProvider>
                        );
                    }
                })
                .catch((err) => console.log("Error retrieving cart", err));
        }

        const initCartActions = (cartStore) => {
            const products = document.getElementsByClassName("product-card");

            for (let product of products) {
                const id = product.dataset.product;
                const reactNode = product.querySelector(".react-cart-actions");

                createRoot(reactNode).render(
                    <IntlProvider {...this.intlProviderProps}>
                        <CartProduct store={cartStore} productId={id} />
                    </IntlProvider>
                );
            }
        };
    }
}
