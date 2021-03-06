import { observable, action, computed } from "mobx";
import { CartProductConsumer } from "./../data/shop/cart";

export class CartStore {
    @observable products = [];
    @observable user = {};
    id = null;
    @observable status = null;

    constructor(cart) {
        this.products = cart.products.map(cp => new CartProduct(cp));
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
            .then(resp => this.products.push(new CartProduct(resp)))
            .catch(err => console.log("Error adding product", err));
    }

    @action removeProduct(id) {
        this.cartProductConsumer
            .removeProduct(id)
            .then(() => {
                this.products = this.products.filter(p => p.id !== id);
            })
            .catch(err => console.log("error deleting product", err));
    }

    @action clearCart() {
        this.products.clear();
    }

    /**
     * Find cart product by it's product's id
     * @param id
     * @returns {*}
     */
    findProduct(id) {
        return this.products.find(cp => Number(cp.product.id) === Number(id));
    }

    @action changeAmount(productId, amount) {
        const cartProduct = this.findProduct(productId);
        const cpAmount = cartProduct.amount + amount;

        if (cpAmount === 0) {
            this.removeProduct(cartProduct.id);
        } else {
            this.cartProductConsumer
                .updateAmount(cartProduct.id, cpAmount)
                .then(() => (cartProduct.amount = cpAmount))
                .catch(err => console.log("could not update amount", err));
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

    @computed get totalStr() {
        return (this.amount * this.product.price).toFixed(2);
    }
}
