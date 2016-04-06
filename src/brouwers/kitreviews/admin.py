from django.contrib import admin
from models import KitReview, KitReviewVote, KitReviewProperty, KitReviewPropertyRating


class KitReviewPropertyRatingInline(admin.TabularInline):
    model = KitReviewPropertyRating
    list_display = ('rating',)


@admin.register(KitReview)
class KitReviewAdmin(admin.ModelAdmin):
    list_display = ('model_kit', 'reviewer', 'submitted_on', 'last_edited_on')
    list_filter = ('reviewer', 'submitted_on')
    search_fields = ('model_kit__name', 'reviewer__username', 'brand__name')
    inlines = [KitReviewPropertyRatingInline]


@admin.register(KitReviewVote)
class KitReviewVoteAdmin(admin.ModelAdmin):
    list_display = ('kit_review', 'voter', 'vote')


@admin.register(KitReviewProperty)
class KitReviewPropertyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
