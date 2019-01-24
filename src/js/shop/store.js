import { observable, action, computed } from "mobx";
import { CartProductConsumer } from "./../data/shop/cart";

export class CartStore {
    @observable products = [];
    @observable user = {};
    id = null;

    constructor(cart) {
        this.products = cart.products.map(
            product => new CartProduct(product, this)
        );
        this.cartProductConsumer = new CartProductConsumer();
        this.id = cart.id;
        this.user = cart.user;
    }

    @computed get total() {
        const total = this.products.reduce((acc, curr) => acc + curr.total, 0);
        return total.toFixed(2);
    }

    @computed get amount() {
        return this.products.reduce((acc, curr) => acc + curr.amount, 0);
    }

    @action addProduct(data) {
        return this.cartProductConsumer
            .addProduct(data)
            .then(resp => {
                const p = new CartProduct(resp, this);
                this.products.push(p);
            })
            .catch(err => console.log("Error adding product", err));
    }

    @action removeProduct(product) {
        this.products = this.products.filter(p => p.id !== product.id);
    }

    @action clearCart() {
        this.products = [];
    }

    findProduct(id) {
        return this.products.find(cp => Number(cp.product.id) === Number(id));
    }

    @action changeAmount(id, amount) {
        const cartProduct = this.findProduct(id);
        cartProduct.amount += amount;

        if (cartProduct.amount === 0) {
            this.removeProduct(cartProduct);
        }
    }
}

export class CartProduct {
    id = null;
    store = null;
    cartId = null;
    product = null;
    @observable amount = 0;

    constructor(cartProduct = {}, store) {
        this.store = store;
        this.id = cartProduct.id;
        this.amount = cartProduct.amount;
        this.cartId = cartProduct.cart;
        this.product = cartProduct.product;
    }

    @action increaseAmount(amount) {
        this.amount += amount;
    }

    @action decreaseAmount(amount) {
        this.amount -= amount;
    }

    @computed get total() {
        return this.amount * this.product.price;
    }
}
