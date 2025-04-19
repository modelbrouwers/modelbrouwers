import {action, computed, makeObservable, observable} from 'mobx';

import {deleteCartProduct, patchCartProductAmount} from './../data/shop/cart';

export class CartStore {
  products = [];
  user = {};
  id = null;
  status = null;

  constructor(cart) {
    makeObservable(this, {
      products: observable,
      user: observable,
      status: observable,
      total: computed,
      amount: computed,
      removeProduct: action,
      clearCart: action,
      changeAmount: action,
    });

    this.products = cart.products.map(cp => new CartProduct(cp));
    this.id = cart.id;
    this.user = cart.user;
  }

  get total() {
    const total = this.products.reduce((acc, curr) => acc + curr.total, 0);
    return total.toFixed(2);
  }

  get amount() {
    return this.products.reduce((acc, curr) => acc + curr.amount, 0);
  }

  removeProduct(id) {
    deleteCartProduct(id)
      .then(() => {
        this.products = this.products.filter(p => p.id !== id);
      })
      .catch(err => console.log('error deleting product', err));
  }

  clearCart() {
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

  changeAmount(productId, amount) {
    const cartProduct = this.findProduct(productId);
    const cpAmount = cartProduct.amount + amount;

    if (cpAmount <= 0) {
      this.removeProduct(cartProduct.id);
    } else {
      patchCartProductAmount(cartProduct.id, cpAmount)
        .then(() => cartProduct.setAmount(cpAmount))
        .catch(err => console.log('could not update amount', err));
    }
  }
}

export class CartProduct {
  id = null;
  store = null;
  cartId = null;
  product = null;
  amount = 0;

  constructor(cartProduct = {}, store) {
    makeObservable(this, {
      amount: observable,
      setAmount: action,
      total: computed,
      totalStr: computed,
    });

    this.store = store;
    this.id = cartProduct.id;
    this.amount = cartProduct.amount;
    this.cartId = cartProduct.cart;
    this.product = cartProduct.product;
  }

  setAmount(amount) {
    this.amount = amount;
  }

  get total() {
    return this.amount * this.product.price;
  }

  get totalStr() {
    return (this.amount * this.product.price).toFixed(2);
  }
}
