from django.conf import settings

from webtest.forms import Text


class LoginRequiredMixin(object):
    def _test_login_required(self, url, response=None):
        if response is None:
            response = self.app.get(url)
        redirect = u"{}?next={}".format(settings.LOGIN_URL, url)
        self.assertRedirects(response, redirect)


class WebTestFormMixin(object):

    def _add_field(self, form, name, value):
        def get_pos(item):
            if isinstance(item, list):
                return item[0].pos
            else:
                return item.pos

        max_pos = max([get_pos(x) for x in form.fields.values()])
        field = Text(form, 'input', None, max_pos + 1, value)
        form.fields[name] = field
        form.field_order.append((name, field))
        return field
