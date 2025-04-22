import type {CountryOption} from '@/components/forms/CountryField';

export interface Customer {
  firstName: string;
  lastName: string;
  email: string;
  phone: string;
}

export interface Address {
  company: string;
  chamberOfCommerce: string;
  street: string;
  number: string;
  city: string;
  postalCode: string;
  country: CountryOption['value'];
}

interface PickupDelivery {
  deliveryMethod: 'pickup';
  deliveryAddress: null;
  billingAddress: null;
}

interface MailDelivery {
  deliveryMethod: 'mail';
  deliveryAddress: Address;
  billingAddress: Address | null;
}

export type DeliveryDetails = (PickupDelivery | MailDelivery) & {
  customer: Customer;
};

export interface PaymentDetails {
  paymentMethod: number;
  paymentMethodOptions: null | Record<string, any>;
}

/**
 * Matches the backend serializer exposing the user details.
 *
 * @see `brouwers.users.api.serializers.UserWithProfileSerializer`
 */
export interface UserData {
  username: string;
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  profile: {
    street: string;
    number: string;
    postal: string;
    city: string;
    country: CountryOption['value'] | 'F' | '';
  };
}

/**
 * Matches the backend serializer processing the address data.
 *
 * @see `brouwers.shop.serializers.AddressSerializer`
 */
export interface AddressData {
  street: string;
  number: string;
  postal_code: string;
  city: string;
  country: Address['country'];
  company: string;
  chamber_of_commerce: string;
}

/**
 * Matches the backend serializer processing the checkout data.
 *
 * @see `brouwers.shop.serializers.ConfirmOrderSerializer`
 */
export interface ConfirmOrderData {
  first_name: string;
  last_name: string;
  email: string;
  phone: string; // may be empty
  delivery_method: DeliveryDetails['deliveryMethod'];
  /**
   * Delivery address is `null` when delivery method pickup is chosen.
   */
  delivery_address: null | AddressData;
  /**
   * Invoice address is `null` when delivery method pickup is chosen, or it's the same
   * as the delivery address.
   */
  invoice_address: null | AddressData;
  /**
   * Primary key of the cart being checkout out.
   */
  cart: number;
  /**
   * Primary key of the selected payment method.
   */
  payment_method: number;
  /**
   * The shape of the payment options is determined by the selected payment method.
   */
  payment_method_options: null | Record<string, any>;
}

export type OrderDetails = null | {
  number: string;
  message: string;
};

/**
 * Matches the backend serializer processing the checkout data.
 *
 * @see `brouwers.shop.serializers.ConfirmOrderSerializer`
 */
export interface CheckoutValidationErrors {}
