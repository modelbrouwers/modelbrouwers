# Shop questions/design decisions

## Current status

### Admin interface

Minimal / bare-bones -> not very user friendly.

- Products in admin with translation options - can definitely use more help texts though

  - SEO metadata
  - Product images (TODO: inline)
  - Product brands (unused in old shop? vs. manufacturer)

- Managing categories tree
- Categories to highlight on homepage + carousel images
- Configuration: Sisow details
- Configure payment options
- Keeping track of shopping carts + snapshots
- Keeping track of shopping orders / addresses
- Keeping track of shopping payments
- Import/export from/to Excel (and other formats)

### Public UI

**Homepage**

- Categories highlighted (optionally expose subset of nested categories)
- Carousel with images/slides (TODO: link to relevant page?)
- Search is placeholder

**Catalog view**

- Responsive design (mobile first, accessibility)\
- Tree view of categories
- Grid view of products (fallback image if none exists etc.)
- Quick "add to cart" + modify amount after adding.
- Mini-cart view in header

**Product detail**

- Responsive layout is TODO
- Enter number to add X to cart
- Description
- Reviews tab

**View cart**

- Overview in tabular form
- Modify amounts

**Checkout**

- Responsive
- Login / checkout anonymous
- If authenticated -> data from profile prefilled
- Personal details + address details
- Payment: select method + additional details depending on method
- Displaying validation errors
- iDeal payment flow
- Mister Cash payment flow

## Features to scrap/abandon

**Product detail**

- Product reviews -> used? relevant?
- Wishlist (easy to implement)
- Product comparison (harder to implement)

**Catalog view**

- Wishlist (easy to implement)
- Product comparison (harder to implement)

## Features missing

### Admin

- Shipping costs calculation
- What about order history from old shop? Legal requirements?
- GDPR/AVG history cleaning (either automated or manual -> provide filter/selection controls)
- Shipping provider connection (Sendcloud)
- Migrate user accounts from old shop
- e-mail template management (!)
- voucher system

### Public UI

**Product detail**

- Mobile styling
- ...

**URLs**

- Ensure that language-specific URLs are supported
- Ensure old URLs at least have redirects
- Keep URL structure intact

**Checkout**

- Payment validation errors display
- Styling / design
- Confirmation page with succesful payment
- Shipping costs calculation + display
- Bank transfer + Paypal payment methods
- Testing Sofort
- Invoicing/invoice generation?

**Homepage**

- Make more attractive? Designs?

### Point of Sale

- still completely to build
- will take a look at existing solution probably and mimick that? But please provide
  wishes for what would work best at all!

### Misc

- payment by crypto?
- Dymo label writer -> looks complex
- A customer loyalty system where they collect 'points' which can lead to
  reductions on the next order.
