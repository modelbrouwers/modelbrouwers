from django.contrib import admin
from models import *

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

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'in_use')
    search_fields = ('question',)

class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ('answer',)

class SoftwareVersionAdmin(admin.ModelAdmin):
    list_diplsay = ('__unicode__', 'start', 'end')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(RegistrationQuestion, QuestionAdmin)
admin.site.register(QuestionAnswer, QuestionAnswerAdmin)
admin.site.register(SoftwareVersion, SoftwareVersionAdmin)
