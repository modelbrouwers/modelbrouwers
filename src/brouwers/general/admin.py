from django.contrib import admin

from .models import (
    Announcement,
    QuestionAnswer,
    RegistrationAttempt,
    RegistrationQuestion,
    UserProfile,
)


class UserProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ('General', {
            'fields': ('user', 'forum_nickname')
        }),
        ('Awards', {
            'fields': (('last_vote', 'exclude_from_nomination'), 'categories_voted')
        }),
        ('Address', {
            'fields': (
                ('street', 'number'),
                ('postal', 'city'),
                ('province', 'country'),
            )
        })
    )

    list_display = ('forum_nickname', 'user', 'full_name', 'exclude_from_nomination', 'last_vote')
    list_filter = ('allow_sharing', 'exclude_from_nomination')
    search_fields = ('forum_nickname', 'user__email')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'in_use')
    search_fields = ('question',)
    filter_horizontal = ('answers',)


class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ('answer',)


class RegistrationAttemptAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'question_short', 'answer', 'timestamp', 'ip_address', 'success',
                    '_is_banned', 'type_of_visitor')
    list_filter = ('success', 'timestamp', 'type_of_visitor')
    search_fields = ('username',)
    actions = None


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'from_date', 'to_date')
    list_filter = ('language', 'from_date', 'to_date')
    list_editable = ('from_date', 'to_date')
    search_fields = ('text',)


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(RegistrationQuestion, QuestionAdmin)
admin.site.register(QuestionAnswer, QuestionAnswerAdmin)
admin.site.register(RegistrationAttempt, RegistrationAttemptAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
