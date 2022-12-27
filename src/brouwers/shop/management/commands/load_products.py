from decimal import Decimal

from django.core.management import BaseCommand
from django.db import transaction
from django.utils import translation

from tablib import import_set

from ...constants import WeightUnits
from ...models import Product, ProductManufacturer

VAT_MAPPING = {
    "BTW Hoog": Decimal("0.21"),
    "BTW Laag": Decimal("0.06"),
    "--- None ---": Decimal("0"),
}

WEIGHT_UNIT_MAPPING = {
    "Gram": WeightUnits.gram,
}


def unescape(text):
    return (
        (text or "")
        .replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&quot;", '"')
        .replace("&#39;", "'")
    )


class Command(BaseCommand):
    help = "Load categories from OpenCart export into database"

    def add_arguments(self, parser):
        parser.add_argument("infile", nargs="+", help="path to the XLSX file to load")

    @transaction.atomic
    def handle(self, **options):
        translation.activate("nl")

        datasets = []
        # convert xlsx files into datasets
        for path in options["infile"]:
            with open(path, "rb") as infile:
                datasets.append(import_set(infile.read(), format="xlsx"))

        # merge datasets together
        def get_lines():
            for ds in datasets:
                for line in ds.dict:
                    yield line

        # get all the manufacturers
        manufacturers = {}
        manufacturer_names = set()
        for line in get_lines():
            manufacturer_names.add(line["Manufacturer"])

        for name in manufacturer_names:
            manufacturers[name], _ = ProductManufacturer.objects.get_or_create(
                name=name
            )

        # load the products
        products = []
        slugs_seen = set()
        for line in get_lines():
            slug = line["SEO Keyword"]
            if not slug or slug in slugs_seen:
                _prod = Product(name=line["Name"])
                slug = Product._meta.get_field("slug").pre_save(_prod, None)

                if slug in slugs_seen:
                    slug += "-1"

            slugs_seen.add(slug)

            products.append(
                Product(
                    id=int(line["Product ID"]),
                    name=line["Name"],
                    # FIXME - for uniqueness constraint
                    slug_nl=slug,
                    slug_en=slug,
                    slug_de=slug,
                    model_name=line["Model"],
                    stock=max(int(line["Quantity"]), 0),
                    price=Decimal(line["Price"]),
                    vat=VAT_MAPPING[line["Tax Class"]],
                    description=unescape(line["Description"]),
                    length=Decimal(line["Length"]),
                    width=Decimal(line["Width"]),
                    height=Decimal(line["Height"]),
                    weight=Decimal(line["Weight"]),
                    weight_unit=WEIGHT_UNIT_MAPPING[line["Weight Class"]],
                    manufacturer=manufacturers[line["Manufacturer"]],
                )
            )

        Product.objects.bulk_create(products)

        # set the M2M relations - db intensive!
        for product, line in zip(products, get_lines()):
            # set the product tags
            if line["Tags"]:
                tags = line["Tags"].replace("&amp;", "&")
                tags = [t for t in tags.split(", ") if len(t) <= 100]
                product.tags.set(tags)

            # set the categories
            if line["Categories"]:
                category_ids = [int(x) for x in line["Categories"].split(", ")]
                product.categories.set(category_ids)

            # set the related products
            if line["Related Products"]:
                product_ids = [int(x) for x in line["Related Products"].split(", ")]
                product.related_products.set(product_ids)
