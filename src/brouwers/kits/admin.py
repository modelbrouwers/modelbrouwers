from django import forms
from django.contrib import admin
from django.contrib.admin import helpers
from django.core.exceptions import PermissionDenied
from django.db.models import Prefetch
from django.template.response import TemplateResponse
from django.utils.encoding import force_str
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from brouwers.builds.models import Build
from brouwers.utils.admin.decorators import link_list

from .models import Boxart, Brand, ModelKit, Scale


def merge_duplicates(modeladmin, request, queryset):
    """
    Marks the queryset objects as duplicates.

    This needs an intermediate page to select which object it's a duplicate of.
    """
    if not request.user.is_superuser:
        raise PermissionDenied

    opts = modeladmin.model._meta

    # create the form
    target_queryset = modeladmin.model.objects.exclude(
        pk__in=queryset.values_list("pk", flat=True)
    )
    DuplicateForm = type(
        "DuplicateForm",
        (forms.Form,),
        {
            "target": forms.ModelChoiceField(
                queryset=target_queryset, empty_label=None, label=_("merge into")
            )
        },
    )

    if request.POST.get("post"):
        form = DuplicateForm(request.POST)
        if form.is_valid():
            target = form.cleaned_data["target"]
            for item in queryset:
                item.modelkit_set.update(**{opts.model_name: target})

            queryset.delete()
            # Return None to display the change list page again.
            return None

    if len(queryset) == 1:
        objects_name = force_str(opts.verbose_name)
    else:
        objects_name = force_str(opts.verbose_name_plural)

    context = {
        "title": _("Merge duplicates"),
        "queryset": queryset,
        "form": DuplicateForm(),
        "objects_name": objects_name,
        "opts": opts,
        "action_checkbox_name": helpers.ACTION_CHECKBOX_NAME,
    }
    return TemplateResponse(request, "admin/kits/mark_duplicate.html", context)


merge_duplicates.short_description = _("Merge selected %(verbose_name_plural)s")


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "logo", "is_active", "slug")
    list_filter = ("is_active",)
    search_fields = ("=id", "name")
    actions = [merge_duplicates]


@admin.register(Scale)
class ScaleAdmin(admin.ModelAdmin):
    list_display = ("__str__",)
    search_fields = ("scale",)
    actions = [merge_duplicates]


@admin.register(ModelKit)
class ModelKitAdmin(admin.ModelAdmin):
    list_display = ("name", "brand", "scale", "get_builds", "get_box_image_url")
    list_filter = ("is_reviewed", "brand", "scale")
    search_fields = ("name", "kit_number")
    raw_id_fields = ("submitter", "duplicates")

    def get_queryset(self, request=None):
        prefetch = Prefetch("builds", queryset=Build.objects.select_related("user"))
        return super().get_queryset(request=request).prefetch_related(prefetch)

    @link_list(short_description=_("builds"))
    def get_builds(self, obj):
        return obj.builds.all()

    def get_box_image_url(self, obj) -> str:
        if not obj.box_image:
            return ""
        tpl = '<a href="{href}" target="_blank" rel="norel noopener">{text}</a>'
        return format_html(tpl, href=obj.box_image.url, text=_("view image"))

    get_box_image_url.short_description = _("boxart")


@admin.register(Boxart)
class BoxartAdmin(admin.ModelAdmin):
    list_display = ["uuid", "image"]
    list_filter = ["created"]
