from django import template
from django.template import Library, TemplateSyntaxError

from ..models import Category

register = Library()


@register.simple_tag
def category_tree(**extra_filters):
    default_filters = {"enabled": True, "depth__lte": 2}
    filters = {**default_filters, **extra_filters}
    qs = Category.get_tree().filter(**filters)
    return Category.get_annotated_list_qs(qs)


@register.simple_tag
def is_in_branch(node1, node2) -> bool:
    """
    Check whether node1 and node2 are in the same branch.

    Node 1 should be the node expected to be closer to the leaf, while node 2 is closer
    to the root.
    """
    if node1 == node2:
        return True
    return node1.is_descendant_of(node2)


class RecordCategoryPathNode(template.Node):
    def __init__(self, item_var, info_var, asvar):
        self.item_var = item_var
        self.info_var = info_var
        self.asvar = asvar

    def render(self, context):
        category = self.item_var.resolve(context)
        info = self.info_var.resolve(context)

        # track the tree walking state
        if self not in context.render_context:
            context.render_context[self] = {
                "branch": [],
                "prev_info": None,
            }

        branch = context.render_context[self]["branch"]
        prev_info = context.render_context[self]["prev_info"]
        if prev_info is not None:
            if info["level"] == prev_info["level"]:
                branch.pop(-1)  # prop previous node off so it can be replaced
            elif (diff := prev_info["level"] - info["level"]) > 0:
                branch = branch[: -(diff + 1)]
                context.render_context[self]["branch"] = branch

        branch.append(category)

        # calculate the full path of the entire branch
        path = "/".join(cat.slug for cat in branch)
        context[self.asvar] = path

        context.render_context[self]["prev_info"] = info
        return ""


@register.tag(name="record_category_path")
def do_record_category_path(parser, token):
    args = token.split_contents()
    if len(args) != 5:
        raise TemplateSyntaxError("'record_category_path' requires five arguments")
    if args[-2] != "as":
        raise TemplateSyntaxError("'record_category_path' requires the 'as foo' form ")

    item_var, info_var, asvar = args[1], args[2], args[4]
    return RecordCategoryPathNode(
        parser.compile_filter(item_var),
        parser.compile_filter(info_var),
        asvar,
    )
