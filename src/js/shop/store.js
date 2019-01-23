import { observable, action } from "mobx";

class CartProductStore {
    @observable cartProducts;

    constructor() {
        this.cartProducts = [];
    }

    setProducts(cartProducts) {
        this.cartProducts = cartProducts;
    }

    getByProductId(id) {
        return this.cartProducts.find(cp => cp.product.id === Number(id));
    }

    @action changeAmount(id, amount) {
        const cartProduct = this.cartProducts.find(cp => cp.id === id);
        if (cartProduct.amount > 0 || amount > 0) {
            cartProduct.amount += amount;

            this.cartProducts = [
                ...this.cartProducts.filter(cp => cp.id !== id),
                cartProduct
            ];
        }
    }
}

class CartStore {
    @observable cart = {};
}

const cartProductStore = new CartProductStore();

export { cartProductStore };
