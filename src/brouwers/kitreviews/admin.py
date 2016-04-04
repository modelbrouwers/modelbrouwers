from django.contrib import admin
from models import KitReview, KitReviewVote, KitReviewProperty


@admin.register(KitReview)
class KitReviewAdmin(admin.ModelAdmin):
    list_display = ('model_kit', 'rating', 'reviewer', 'submitted_on', 'last_edited_on')
    list_filter = ('rating', 'reviewer', 'submitted_on')
    search_fields = ('model_kit__name', 'reviewer__username', 'brand__name')


@admin.register(KitReviewVote)
class KitReviewVoteAdmin(admin.ModelAdmin):
    list_display = ('kit_review', 'voter', 'vote')


@admin.register(KitReviewProperty)
class KitReviewPropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating')
    search_fields = ('name',)
