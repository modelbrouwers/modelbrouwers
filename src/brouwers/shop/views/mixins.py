from django.contrib.auth.mixins import PermissionRequiredMixin

from brouwers.utils.tests import is_testing


class TestPermissionsRequiredMixin(PermissionRequiredMixin):
    permission_required = "shop.add_product"
    raise_exception = True

    def has_permission(self):  # pragma: no cover
        if is_testing():
            return True
        return super().has_permission()
