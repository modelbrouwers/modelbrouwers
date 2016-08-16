from django.contrib import admin

from .models import (
    KitReview, KitReviewProperty, KitReviewPropertyRating, KitReviewVote
)


class KitReviewPropertyRatingInline(admin.TabularInline):
    model = KitReviewPropertyRating
    list_display = ('rating',)
    extra = 0


class KitReviewVoteInline(admin.TabularInline):
    model = KitReviewVote
    raw_id_fields = ('voter',)
    extra = 0


@admin.register(KitReview)
class KitReviewAdmin(admin.ModelAdmin):
    list_display = ('model_kit', 'reviewer', 'submitted_on', 'last_edited_on')
    list_filter = ('submitted_on',)
    search_fields = ('model_kit__name', 'reviewer__username', 'model_kit__brand__name')
    inlines = [KitReviewPropertyRatingInline, KitReviewVoteInline]
    raw_id_fields = ['model_kit', 'album', 'reviewer']


@admin.register(KitReviewVote)
class KitReviewVoteAdmin(admin.ModelAdmin):
    list_display = ('kit_review', 'voter', 'vote')
    readonly_fields = ('kit_review', 'voter')


@admin.register(KitReviewProperty)
class KitReviewPropertyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
