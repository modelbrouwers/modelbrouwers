import rest_framework_filters as filters

from ..models import User


class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = ("id", "username")
