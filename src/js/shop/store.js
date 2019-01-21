import { observable, computed } from "mobx";

class CartProductStore {
    @observable products;

    constructor() {
        this.products = [];
    }

    setProducts(products) {
        this.products = products;
    }

    @computed getProductById() {
        return this.products.find(product => product.id === id);
    }
}

const cartProductStore = new CartProductStore();

export { cartProductStore };
