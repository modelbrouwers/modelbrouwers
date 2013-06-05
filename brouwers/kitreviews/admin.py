from django.contrib import admin
from models import *

class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)

class ScaleAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'scale')
    list_editable = ('scale',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'name',)
    list_editable = ('name',)
    search_fields = ('name',)

class ModelKitAdmin(admin.ModelAdmin):
    list_display = ('brand', 'name', 'kit_number', 'scale', 'submitter', 'submitted_on')
    list_filter = ('brand', 'scale', 'submitter', 'submitted_on')
    search_fields = ('name', 'brand__name', 'submitter__username', 'kit_number')
    list_editable = ('name',)

class KitReviewAdmin(admin.ModelAdmin):
    list_display = ('model_kit', 'rating', 'reviewer', 'submitted_on', 'last_edited_on')
    list_filter = ('rating', 'reviewer', 'submitted_on')
    search_fields = ('model_kit__name', 'reviewer__username', 'brand__name')

class KitReviewVoteAdmin(admin.ModelAdmin):
    list_display = ('kit_review', 'voter', 'vote')

admin.site.register(Brand, BrandAdmin)
admin.site.register(Scale, ScaleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ModelKit, ModelKitAdmin)
admin.site.register(KitReview, KitReviewAdmin)
admin.site.register(KitReviewVote, KitReviewVoteAdmin)