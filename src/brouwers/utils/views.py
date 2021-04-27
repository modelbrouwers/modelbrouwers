from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin  # noqa
from django.utils.decorators import method_decorator


class StaffRequiredMixin(object):
    """Only users with is_staff=True can see this view"""

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
