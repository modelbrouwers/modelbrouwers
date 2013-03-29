from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from models import *

class UserAdmin2(UserAdmin):
    list_editable = ('email',)

class UserProfileAdmin(admin.ModelAdmin):
	fieldsets = (
		('General', {
			'fields': ('user', 'forum_nickname')
		  }),
		('Awards', {
#			'classes': ['collapse'],
			'fields': (('last_vote', 'exclude_from_nomination'), 'categories_voted')
		}),
		('Secret Santa', {
#			'classes': ['collapse'],
			'fields': ('secret_santa', ('street','number'),('postal', 'city'),('province','country'), 'preference', 'refuse')
		})
	)
	
	list_display = ('forum_nickname', 'user', 'full_name', 'exclude_from_nomination', 'last_vote', 'secret_santa')
	search_fields = ('forum_nickname',)

class ForumUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'user_email', 'user_email_hash', 'get_email_hash')
    search_fields = ('username',)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'in_use')
    search_fields = ('question',)

class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ('answer',)

class RegistrationAttemptAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'question', 'answer', 'timestamp', 'ip_address', 'success')
    list_filter = ('success', 'timestamp', 'ip_address', 'username')
    search_fields = ('username',)

class SoftwareVersionAdmin(admin.ModelAdmin):
    list_diplsay = ('__unicode__', 'start', 'end')

class RedirectAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'path_from', 'path_to')
    list_editable = ('path_from', 'path_to')
    search_fields = ('path_from', 'path_to')

class PasswordResetAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'expire', 'h')
    list_filter = ('expire',)

admin.site.unregister(User)
admin.site.register(User, UserAdmin2)

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(ForumUser, ForumUserAdmin)
admin.site.register(RegistrationQuestion, QuestionAdmin)
admin.site.register(QuestionAnswer, QuestionAnswerAdmin)
admin.site.register(RegistrationAttempt, RegistrationAttemptAdmin)
admin.site.register(SoftwareVersion, SoftwareVersionAdmin)
admin.site.register(Redirect, RedirectAdmin)
admin.site.register(PasswordReset, PasswordResetAdmin)
