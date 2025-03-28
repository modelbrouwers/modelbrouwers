import { makeObservable, observable, action, computed } from "mobx";
import { CartProductConsumer } from "../data/shop/cart";

import type { Cart, CartProduct as APICartProduct, Product } from "./types";

interface AddProductData {
    id: number | null;
    product: number;
    amount: number;
    cart: number;
}

export class CartStore {
    products: CartProduct[] = [];
    user = {};
    id: number;
    status = null;

    shippingCosts: number = 0;

    private cartProductConsumer: CartProductConsumer;

    public constructor(cart: Cart) {
        makeObservable(this, {
            products: observable,
            user: observable,
            status: observable,
            shippingCosts: observable,
            total: computed,
            amount: computed,
            addProduct: action,
            removeProduct: action,
            clearCart: action,
            changeAmount: action,
            setShippingCosts: action,
        });

        this.products = cart.products.map((cp) => new CartProduct(cp));
        this.cartProductConsumer = new CartProductConsumer();
        this.id = cart.id;
        this.user = cart.user;
    }

    public get total(): string {
        const totalProducts = this.products.reduce(
            (acc, curr) => acc + curr.total,
            0,
        );
        const total = totalProducts + this.shippingCosts;
        return total.toFixed(2);
    }

    public get amount(): number {
        return this.products.reduce((acc, curr) => acc + curr.amount, 0);
    }

    public addProduct(data: AddProductData) {
        const existingCardProduct = this.findProduct(data.product);
        if (existingCardProduct) {
            return this.changeAmount(data.product, data.amount);
        }
        const postData = { ...data, cart: this.id };
        return this.cartProductConsumer
            .addProduct(postData)
            .then((resp) => this.products.push(new CartProduct(resp)))
            .catch((err) => console.log("Error adding product", err));
    }

    public removeProduct(id: number) {
        this.cartProductConsumer
            .removeProduct(id)
            .then(() => {
                this.products = this.products.filter((p) => p.id !== id);
            })
            .catch((err: unknown) =>
                console.log("error deleting product", err),
            );
    }

    public clearCart() {
        // @ts-expect-error
        this.products.clear();
    }

    /**
     * Find cart product by it's product's `id`.
     */
    private findProduct(id: number): CartProduct | undefined {
        return this.products.find((cp) => Number(cp.product.id) === Number(id));
    }

    public changeAmount(productId: number, amount: number): void {
        const cartProduct = this.findProduct(productId);
        if (!cartProduct) throw new Error("Product not found.");

        const cpAmount = cartProduct.amount + amount;

        if (cpAmount <= 0) {
            this.removeProduct(cartProduct.id!);
        } else {
            this.cartProductConsumer
                .updateAmount(cartProduct.id, cpAmount)
                .then(() => cartProduct.setAmount(cpAmount))
                .catch((err: unknown) =>
                    console.log("could not update amount", err),
                );
        }
    }

    public setShippingCosts(costs: number): void {
        this.shippingCosts = costs;
    }
}

export class CartProduct {
    id: number | null = null;
    cartId: number;
    product: Product;
    amount = 0;

    public constructor(cartProduct: APICartProduct) {
        makeObservable(this, {
            amount: observable,
            setAmount: action,
            increaseAmount: action,
            decreaseAmount: action,
            total: computed,
            totalStr: computed,
        });

        this.id = cartProduct.id;
        this.amount = cartProduct.amount;
        this.cartId = cartProduct.cart;
        this.product = cartProduct.product;
    }

    public setAmount(amount: number) {
        this.amount = amount;
    }

    public increaseAmount(amount: number) {
        this.amount += amount;
    }

    public decreaseAmount(amount: number) {
        this.amount -= amount;
    }

    public get total(): number {
        return this.amount * this.product.price;
    }

    public get totalStr(): string {
        return (this.amount * this.product.price).toFixed(2);
    }
}
