# Payments via Sisow

Note that you'll need a merchant ID and merchant Key configured in the admin.

You also need to enable testing mode. Currently a merchant key cannot be given,
because it's used in production. There's an open support issue to Sisow about
this. You can mock some function calls if needed.

Quick links:

* [Status](#status)
* [Python code](#python-code)

## Status

Currently, implementing payments through Sisow is work in progress:

* iDeal
    - ~~Starting an iDeal payment~~
    - Handling a succesful iDeal payment
    - Handling a failed iDeal payment
    - Handling a cancelled iDeal payment

* bank transfers
    - starting a payment
    - ?

* Paypal
    - starting a payment
    - handling success
    - handling failure
    - handling cancellation

* Mister cash
    - starting a payment
    - handling success
    - handling failure
    - handling cancellation

* Sofort
    - starting a payment
    - handling success
    - handling failure
    - handling cancellation

## Python code

The entrypoints here are stable-ish. The interface should not change, unless
there's a major design issue.

Example usage on: http://localhost:8000/winkel/pay/. The views are in
`brouwers.winkel.payment.debug_views`

### iDeal

**Getting a list of banks**

Call `brouwers.shop.payments.sisow.get_ideal_bank_choices` for a list of
iDeal bank IDs and names:

```python
>>> from brouwers.shop.payments.sisow import get_ideal_bank_choices
>>> choices = list(get_ideal_bank_choices())
>>> choices
[('99', 'Sisow Bank (test)')]
```

This could/should be added as an API endpoint for when the iDeal payment option
is chosen.

**Starting a transaction**

```python
>>> from brouwers.shop.payments.sisow import start_ideal_payment, iDealBank
>>> redirect_url = start_ideal_payment(
        amount=decimal_amount_in_euros,
        bank=iDealBank(_id="99", name="Sisow Bank (test)")
    )
```

The `redirect_url` is an actual, external URL to redirect the end-user to,
which will perform the actual payment.
