from django.contrib import admin

from .models import Brouwersdag, Competition, Exhibitor, ShowCasedModel


@admin.register(ShowCasedModel)
class ShowCasedModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'scale', 'length', 'width', 'height', 'is_competitor', 'id')
    list_filter = ('competition', 'is_competitor', 'is_paid', 'brouwersdag', 'scale')
    search_fields = ('competition__name', 'name', 'owner__username')


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'name', 'max_num_models', 'max_participants', 'is_current')
    list_editable = ('name', 'max_num_models', 'max_participants', 'is_current')
    search_fields = ('name',)


class ExhibitorInline(admin.TabularInline):
    model = Exhibitor


@admin.register(Brouwersdag)
class BrouwersdagAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')
    list_editable = ('date',)
    search_fields = ('name',)
    inlines = [ExhibitorInline]
