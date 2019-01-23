import { observable, action, computed } from "mobx";

class CartProductStore {
    @observable cartProducts;

    constructor() {
        this.cartProducts = [];
    }

    setProducts(cartProducts) {
        this.cartProducts = cartProducts;
    }

    getByProductId(id) {
        return this.cartProducts.find(
            cp => Number(cp.product.id) === Number(id)
        );
    }
}

class CartStore {
    @observable cart = {
        products: []
    };

    @action addProduct(product) {
        this.cart.products.push(product);
    }

    @action removeProduct(product) {
        this.cart.products = this.cart.products.filter(
            p => p.id !== product.id
        );
    }

    @action clearCart() {
        this.cart.products = [];
    }

    findProduct(id) {
        return this.cart.products.find(
            cp => Number(cp.product.id) === Number(id)
        );
    }

    @computed get total() {
        return this.cart.products.reduce(
            (acc, curr) => acc + (curr.amount * curr.total).toFixed(2)
        );
    }

    @action changeAmount(id, amount) {
        const cartProduct = this.findProduct(id);
        cartProduct.amount += amount;
        if (cartProduct.amount === 0) {
            this.removeProduct(cartProduct);
        }
    }
}

const cartProductStore = new CartProductStore();
const cartStore = new CartStore();

export { cartProductStore, cartStore };
