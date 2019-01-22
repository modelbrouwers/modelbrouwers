import { observable, action } from "mobx";

class CartProductStore {
    @observable products;

    constructor() {
        this.products = [];
    }

    setProducts(products) {
        this.products = products;
    }

    @action getProductById(id) {
        return this.products.find(product => product.id === id);
    }
}

const cartProductStore = new CartProductStore();

export { cartProductStore };
