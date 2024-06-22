import { CountryOption } from "@/components/forms/CountryField";

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
  country: CountryOption["value"];
}

interface PickupDelivery {
  deliveryMethod: "pickup";
  deliveryAddress: null;
  billingAddress: null;
}

interface MailDelivery {
  deliveryMethod: "mail";
  deliveryAddress: Address;
  billingAddress: Address | null;
}

export type DeliveryDetails = (PickupDelivery | MailDelivery) & {
  customer: Customer;
};
