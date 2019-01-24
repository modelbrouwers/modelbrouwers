import React from "react";
import ReactDOM from "react-dom";
import { CartConsumer } from "../data/shop/cart";
import { Cart, CartProduct } from "./components/Cart";
import { CartStore } from "./store";

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
                    let cartStore = new CartStore(cart);
                    initCartActions(cartStore);
                    ReactDOM.render(<Cart store={cartStore} />, node);
                })
                .catch(err => console.log("Error retrieving cart", err));
        }

        const initCartActions = cartStore => {
            const products = document.getElementsByClassName("product-card");

            for (let product of products) {
                const id = product.dataset.product;
                const cartProduct = cartStore.findProduct(id);
                const reactNode = product.querySelector(".react-cart-actions");

                ReactDOM.render(
                    <CartProduct
                        store={cartStore}
                        cartProduct={cartProduct}
                        productId={id}
                    />,
                    reactNode
                );
            }
        };
    }
}
