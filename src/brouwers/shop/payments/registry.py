from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Callable, Optional, Type, TypedDict, Union

from django.http import HttpRequest
from django.http.response import HttpResponseBase
from django.utils.functional import Promise
from django.utils.translation import gettext_lazy as _

from ..models import Order, Payment

__all__ = ["register", "PaymentContext", "Plugin"]

PluginType = Type["Plugin"]
LazyStr = Union[Promise, str]


class PaymentContext(TypedDict):
    request: HttpRequest
    next_page: str
    order: Optional[Order]


@dataclass
class Plugin(ABC):
    identifier: str
    registry: "Registry" = field(init=False)
    verbose_name: LazyStr = field(
        default=_("Set the 'verbose_name' attribute for a human-readable name"),
        init=False,
    )

    def get_label(self):
        return self.verbose_name

    @abstractmethod
    def start_payment(
        self, payment: Payment, context: PaymentContext
    ) -> Optional[HttpResponseBase]:  # pragma: no cover
        """
        Given a payment instance, handle the actual payment flow.

        Returns an HTTP response-like result, or None. If None is returned,
        nothing has to be done.
        """
        pass

    def get_confirmation_message(self, order: Order) -> str:
        return ""


class Registry:
    """
    Payment provider options registry.
    """

    def __init__(self):
        self._registry = {}

    def __call__(self, unique_identifier: str) -> Callable[[PluginType], PluginType]:
        def decorator(plugin_cls: PluginType) -> PluginType:
            if unique_identifier in self._registry:
                raise ValueError(
                    f"The unique identifier '{unique_identifier}' is already present "
                    "in the registry."
                )
            plugin = plugin_cls(identifier=unique_identifier)
            plugin.registry = self
            self._registry[unique_identifier] = plugin
            return plugin_cls

        return decorator

    def __iter__(self):
        return iter(self._registry.values())

    def __getitem__(self, key: str):
        return self._registry[key]

    def __contains__(self, key: str):
        return key in self._registry

    def get_choices(self):
        return [(p.identifier, p.get_label()) for p in self]


register = Registry()
