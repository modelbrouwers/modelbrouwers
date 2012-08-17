from django.conf import settings
from django.core.urlresolvers import reverse

class UploadifyMiddleware(object):
    def process_request(self, request):
        try:
            if (request.method == 'POST') and (request.path == reverse('brouwers.albums.ajax_views.uploadify')) and \
                request.POST.has_key(settings.SESSION_COOKIE_NAME):
                request.COOKIES[settings.SESSION_COOKIE_NAME] = request.POST[settings.SESSION_COOKIE_NAME]
        except: #causes viewdoesnotexist errors FIXME
            pass