from django.conf import settings
from django.core.urlresolvers import reverse

class UploadifyMiddleware(object):
    def process_request(self, request):
        if (request.method == 'POST') and \
        (request.path == reverse('albums.ajax_views.uploadify')) and \
        request.POST.has_key(settings.SESSION_COOKIE_NAME):
            cookie = request.POST[settings.SESSION_COOKIE_NAME]
            request.COOKIES[settings.SESSION_COOKIE_NAME] = cookie
        if (request.method == 'POST') and \
        (request.path == reverse('albums.ajax_views.uploadify')) and \
        request.POST.has_key('csrfmiddlewaretoken'):
            request.COOKIES[settings.CSRF_COOKIE_NAME] = request.POST['csrfmiddlewaretoken']
        return None
