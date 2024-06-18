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
  country: "" | CountryOption["value"];
}

export interface AddressDetails {
  customer: Customer;
  deliveryAddress: Address;
  billingAddress: Address | null;
}
