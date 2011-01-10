from django.shortcuts import render_to_response as real_render_to_response
from django.template.context import RequestContext

def render_to_response(request, template, data = {}):
	"""
	Shortcut to render templates, passing a RequestContext as context_instance,
	this way you always have 'user' available in templates.
	"""
	response = real_render_to_response(template, data, context_instance = RequestContext(request))
	return response
