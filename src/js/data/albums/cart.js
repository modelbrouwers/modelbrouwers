import { CrudConsumer, CrudConsumerObject } from "consumerjs";

import { API_ROOT } from "../../constants";

class Cart extends CrudConsumerObject {}

export class CartConsumer extends CrudConsumer {
    constructor(endpoint = `${API_ROOT}api/v1/shop/cart`, objectClass = Cart) {
        super(endpoint, objectClass);
    }

    fetch() {
        return this.get("/");
    }

    rotate(id, direction) {
        const endpoint = `/${id}/rotate/`;
        return this.patch(endpoint, { direction: direction });
    }
}

class CartProduct extends CrudConsumerObject {}

export class CartProductConsumer extends CrudConsumer {
    constructor(
        endpoint = `${API_ROOT}api/v1/shop/cart-product`,
        objectClass = CartProduct
    ) {
        super(endpoint, objectClass);
    }

    getCartProduct(id) {
        return this.get(`/${id}`);
    }

    /**
     * Add product to cart
     * @param {Object} data
     * @property {Number} product - id of the product
     * @property {Number} cart - id of the cart
     * @property {Number} amount - amount of products
     * @returns {Promise}
     */
    addProduct(data) {
        return this.post("/", data);
    }
}
