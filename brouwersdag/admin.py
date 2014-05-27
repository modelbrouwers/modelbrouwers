from django.contrib import admin

from .models import Competition, ShowCasedModel, Brouwersdag, Exhibitor


class ShowCasedModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'scale', 'length', 'width', 'height', 'is_competitor')
    list_filter = ('competition', 'is_competitor', 'is_paid', 'scale')
    search_fields = ('competition__name', 'name', 'owner__username')


class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'name', 'max_num_models', 'max_participants', 'is_current')
    list_editable = ('name', 'max_num_models', 'max_participants', 'is_current')
    search_fields = ('name',)


class ExhibitorInline(admin.TabularInline):
    model = Exhibitor


class BrouwersdagAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')
    list_editable = ('date',)
    search_fields = ('name',)
    inlines = [ExhibitorInline]


admin.site.register(ShowCasedModel, ShowCasedModelAdmin)
admin.site.register(Competition, CompetitionAdmin)
admin.site.register(Brouwersdag, BrouwersdagAdmin)
