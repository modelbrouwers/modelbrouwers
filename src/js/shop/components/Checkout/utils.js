const mandatoryCustomerFields = ["firstName", "lastName", "email"];
const mandatoryAddressFields = [
    "street",
    "number",
    "city",
    "postalCode",
    "country",
];

export const checkAddressFieldsComplete = (customer, deliveryAddress) => {
    const anyMissing =
        mandatoryCustomerFields.some((field) => !customer[field]) ||
        mandatoryAddressFields.some((field) => !deliveryAddress[field]);
    return !anyMissing;
};
