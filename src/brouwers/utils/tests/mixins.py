from django.conf import settings


class LoginRequiredMixin(object):
    def _test_login_required(self, url, response=None):
        if response is None:
            response = self.app.get(url)
        redirect = u"{}?next={}".format(settings.LOGIN_URL, url)
        self.assertRedirects(response, redirect)
