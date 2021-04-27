from django.db import models


class GroupbuildQuerySet(models.QuerySet):
    def with_admin_count(self):
        return self.annotate(n_admins=models.Count("admins"))
