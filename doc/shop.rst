====
Shop
====

Functional requirements for the Modelbrouwers webshop.

.. note::

    We've looked at django-shop and django-oscar first. Both were deemed Not
    Worth The Effort. Django-shop depends on Django-CMS, which has a fairly
    slow release cycle, and there's no need for a CMS in Modelbrouwers.
    Django-Oscar is very powerful, but overkill for Modelbrouwers, and doesn't
    look like it will speed up set-up very much because the principles of Oscar
    need to be learned.

Requirements by Hanjo
=====================

These requirements were given by the owner of Modelbrouwers, so they should
absolutely be implemented in the MVP.

--------------------------------
Public-facing pages requirements
--------------------------------

.. _shop-urls:

Urls
----

Old OpenCart URLs should still work -> the system must be flexible enough to
configure URLs.

Currently, when visiting the shop in another language than Dutch, you get the
'ugly' urls like ``/winkel/index.php?route=product/category&path=94_96``. These
should still work, but *may* be upgraded to proper SEO urls via permanent
redirects.

Payment providers
-----------------

Minimally to be supported:

* iDeal
* pay by bank transfer
* Paypal
* Sofort
* Bancontact/Mister Cash

Currently, Sisow handles this. Sticking with Sisow is preferred for the MVP.

Payment options
---------------

Both checkout with and without account should be possible.

SEO
---

Search engine optimization is critical. All the current meta-data should still
be there in the new site.

Responsive layout
-----------------

It should be easy to browser the shop on Mobile, Tablet and Desktop. This also
bumps our Google ranking (or rather - Google doesn't punish us).

Internationalization
--------------------

Three languages must be supported in the MVP:

* Dutch
* English
* German

This concerns both static translations, and dynamic translations for the actual
shop content/products. Additionally, this also goes down to the URL which should
be internationalized if the :ref:`shop urls` are to be cleaned up.

--------------------
Management interface
--------------------

Adding/modifying products
-------------------------

It should be trivial to modify the catalogue, both in the admin control panel
(= not the django admin!) and via import and export to Excel.

Imagine a flow where prices of all products are bumped by 5% - this is easily
accomplished in Excel. Import and export may be the only implementation for MVP
if it saves time/costs.

-----------------------------------
Migration from OpenCart to new shop
-----------------------------------

The current catalogue (and history) must be migrated to the new shop.

------------------------
Third party integrations
------------------------

A shop has interaction with third party tools to manage the entire flow from
sale to delivery at the door.

Shipping provider connection
----------------------------

There must be an integration with PostNL packet service (currently `Sendcloud`_
is used). It should be easy to print 'send labels'.

Point of Sale
-------------

Modelbrouwers.nl has a physical shop. This means that the webshop should have
an interface that acts as a cash-register. Any sales made in the physical shop
should automatically be reflected in the webshop, such as stock updates.

Product weight
--------------

It must be possible to specify the weight of products, so that the appropriate
shipping box/enveloppe format can be determined to minimize shipping costs.

Wishes by Hanjo
===============

These are nice-to-haves and not required for the MVP.

* Printing addresses for enveloppes, using the *Dymo label writer 400*

* Payment by Bitcoin/other crypto

* A customer loyalty system where they collect 'points' which can lead to
  reductions on the next order.

Technical requirements, based off the current shop in OpenCart
==============================================================

-----
Users
-----

Existing users should be migrated/merged with the users database currently
in Django. This can be based off e-mail address.

----------
Categories
----------

The categories used are simple, there are no multi-category children. Use
django-treebeard with ``MP_Node`` to model this. This also allows for clean
URL generation.

It should be possible to mark a category (root item) as menu item.

On a category page, the sub categories should be listed so that drilldown is
possible.

The category model should have at least the following fields:

* name [translatable]
* slug [translatable, see :ref:`shop-urls`]
* image - thumbnail to use

--------
Products
--------

The core of the webshop are obviously products.

The product model must have at least the following fields:

* name [translatable]
* image [multiple images would be a nice to have]
* make/brand [foreign key field]
* model name [technical code for the model]
* stock/availability
* price
* vat
* description [rich text field (django-ckeditor?)]
* tags [m2m field with tag model]
* related/similar products [m2m, asymmetric/directional?]

Products should also have reviews and ratings. Ratings could be part of reviews.

See exports of the current shop for other missing fields/relevant data that
might need to be migrated.

------------
Translations
------------

django-modeltranslation and django-hvad seem viable packages.
django-modeltranslation has my slight preference since it stores the
translations in the same database table. otoh - hvad uses inner joins with
indexes.

Check support for django 1.10/1.11 for both apps.

---------------
Search function
---------------

Search function should be fast and yield appropriate results. Elastic-search
may be the way to go if searching purely on database is not maintainable.

----
Cart
----

Cart status should be stored in the session and preserved if filling the card
and then logging in.

--------------------------------------------------------------
Downloadable products (generating entrance tickets for events)
--------------------------------------------------------------

* barcodes should be unique (uuid?)
* it should be verifiable that a ticket was scanned or not before
* plugin-like implementation would be great
* generate QR and/or barcode + render to PDF

-----------------------------
Customizable e-mail templates
-----------------------------

mail-editor is a great candidate for this, the idea is that a set of e-mail
types is defined upfront, and in the admin the actual content can be templated
out.

--------
Vouchers
--------

The ability to buy/gift vouchers to people as a product should be kept. A
voucher should also have some sort of unique ID that tracks how much is used,
so people can use a voucher for webshop purchases as well.

-----------------------------------
Carousel/highlighted items homepage
-----------------------------------

There should be a place to enter carousel items/highlighted items. These
should probably just have a reference to the product so the proper URL can be
generated, with image/description/position etc. fields. There should not be any
hardcoding.

---------------
Filter by brand
---------------

The UI should allow a quick search by brand.

---------------
Featured offers
---------------

It should be possible to mark a product as featured offer, with an overridden
price.

------------
New products
------------

New items should be listed. TDB what marks an product as 'new'.


.. _Sendcloud: https://www.sendcloud.nl/
