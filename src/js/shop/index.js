import React from "react";
import ReactDOM from "react-dom";
import { CartConsumer } from "../data/shop/cart";
import { Cart, CartProduct } from "./components/Cart";
import { cartStore } from "./store";

export default class Page {
    static init() {
        this.initRating();
        this.initCart();
    }

    static initRating() {
        const nodes = document.querySelectorAll(".rating-input__star");
        const activeClass = "rating-input__option--is-active";

        if (nodes && nodes.length) {
            for (let node of nodes) {
                node.addEventListener("click", function(e) {
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
        if (node) {
            this.cartConsumer = new CartConsumer();
            this.cartConsumer
                .fetch()
                .then(({ cart }) => {
                    cartStore.cart = cart;
                    initCartActions(cart);
                    ReactDOM.render(<Cart store={cartStore} />, node);
                })
                .catch(err => console.log("Error retrieving cart", err));
        }

        const initCartActions = cart => {
            const products = document.getElementsByClassName("product-card");

            for (let product of products) {
                const id = product.dataset.product;
                const reactNode = product.querySelector(".react-cart-actions");

                ReactDOM.render(
                    <CartProduct
                        store={cartStore}
                        cart={cart}
                        productId={id}
                    />,
                    reactNode
                );
            }
        };
    }
}
