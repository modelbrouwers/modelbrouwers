from django.core.management import BaseCommand

from tablib import import_set

from ...models import Category


class Command(BaseCommand):
    help = "Load categories from OpenCart export into database"

    def add_arguments(self, parser):
        parser.add_argument("infile", help="path to the XLSX file to load")

    def handle(self, **options):
        with open(options["infile"], "rb") as infile:
            dataset = import_set(infile.read(), format="xlsx")

        categories = {}
        children = {}

        for line in dataset.dict:
            # TODO: english & german
            category = dict(
                id=int(line["Category ID"]),
                name_nl=line["Category Name"],
                slug_nl=line["SEO Keyword"],  # don't break existing urls
                image=line["Image"].rsplit("/")[-1],  # TODO: copy image files
                seo_keyword_nl=line["SEO Keyword"],
                enabled=line["Status"] == "Enabled",
            )
            categories[category["id"]] = category

        for line in dataset.dict:
            parent_id = int(line["Parent ID"])
            if not parent_id:
                continue
            child_id = int(line["Category ID"])
            if parent_id not in children:
                children[parent_id] = []
            children[parent_id].append(child_id)

        # turn data into a tree structure and load it with treebeard
        tree_data = []
        child_ids = sum(children.values(), [])
        for category in categories.values():
            has_parent = category["id"] in child_ids
            if has_parent:
                continue

            data = get_data(category, children, categories)
            tree_data.append(data)

        Category.load_bulk(tree_data, parent=None, keep_ids=True)


def get_data(category, children, categories):
    local_child_ids = children.get(category["id"], [])
    local_children = [categories[local_id] for local_id in local_child_ids]
    data = {
        "id": category["id"],
        "data": category,
        "children": [get_data(child, children, categories) for child in local_children],
    }
    return data
