from django import template
from django.template import Library, TemplateSyntaxError

from ..constants import OrderStatuses, PaymentStatuses
from ..models import Category, Order, Payment, Product

register = Library()


@register.simple_tag
def category_tree(max_depth: int = 2, **extra_filters):
    default_filters = {"enabled": True, "depth__lte": max_depth}
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


@register.simple_tag
def get_product_catalogue_path(product: Product, category_path: str) -> str:
    return f"{category_path}/{product.slug}"


class ActiveNodeNode(template.Node):
    def __init__(self, nodes_var, current_node_var, asvar):
        self.nodes_var = nodes_var
        self.current_node_var = current_node_var
        self.asvar = asvar

    def render(self, context):
        nodes = [entry[0] for entry in self.nodes_var.resolve(context)]
        current_node = self.current_node_var.resolve(context)
        if current_node not in nodes:
            # find closest parent
            parents = [
                parent for parent in nodes if current_node.is_descendant_of(parent)
            ]
            current_node = next(
                (n for n in sorted(parents, key=lambda n: n.depth, reverse=True)), None
            )
        context[self.asvar] = current_node
        return ""


@register.tag(name="get_active_node")
def do_get_active_node(parser, token):
    args = token.split_contents()
    assert len(args) == 5
    assert args[-2] == "as"
    nodes_var, current_node_var, asvar = args[1], args[2], args[4]
    return ActiveNodeNode(
        nodes_var=parser.compile_filter(nodes_var),
        current_node_var=parser.compile_filter(current_node_var),
        asvar=asvar,
    )


@register.inclusion_tag("shop/includes/status_progress.html")
def order_status(order: Order):
    # map value -> label
    choices_order = (
        OrderStatuses.received,
        OrderStatuses.processing,
        OrderStatuses.shipped,
    )
    progression = [(value, OrderStatuses.values[value]) for value in choices_order]
    return {"steps": progression, "current": order.status}


@register.inclusion_tag("shop/includes/status_progress.html")
def payment_status(payment: Payment):
    # map value -> label
    choices_order = (PaymentStatuses.pending, PaymentStatuses.completed)
    progression = [(value, PaymentStatuses.values[value]) for value in choices_order]
    return {"steps": progression, "current": payment.status}
