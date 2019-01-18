import React from "react";
import ReactDOM from "react-dom";
import { CartConsumer } from "../data/albums/cart";
import { Cart, CartProduct } from "./components/Cart";

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
                .then(resp => {
                    ReactDOM.render(<Cart cart={resp.cart} />, node);
                    initCartActions(resp.cart);
                })
                .catch(err => console.log("Error retrieving cart", err));
        }

        const initCartActions = cart => {
            const products = document.getElementsByClassName("product-card");

            for (let product of products) {
                const id = product.dataset.product;
                const reactNode = product.querySelector(".react-cart-actions");

                ReactDOM.render(
                    <CartProduct cart={cart} product={id} />,
                    reactNode
                );
            }
        };
    }
}
