from django.conf import settings
from django.shortcuts import render_to_response as real_render_to_response
from django.template.context import RequestContext
from datetime import date

def render_to_response(request, template, data = {}): #DEPRECATED - use django.shortcuts.render
	"""
	Shortcut to render templates, passing a RequestContext as context_instance,
	this way you always have 'user' available in templates.
	"""
	response = real_render_to_response(template, data, context_instance = RequestContext(request))
	return response

def voting_enabled(test_date=date.today()):
	this_year = date.today().year
	vote_start_date = date(this_year, 1, 1)
	vote_end_date = date(this_year, settings.VOTE_END_MONTH, settings.VOTE_END_DAY)
	if test_date <= vote_end_date and test_date >= vote_start_date:
		return True
	return False
