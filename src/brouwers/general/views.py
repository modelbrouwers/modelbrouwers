from django.http import Http404, HttpResponse, JsonResponse
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.views.generic import View

EMPTY_CONTEXT = {}


class ServeHbsTemplateView(View):
    def get(self, request, *args, **kwargs):
        app_name = kwargs.get('app_name')
        template_name = "{template_name}.hbs".format(template_name=kwargs.get('template_name'))

        template_path = "{app_name}/handlebars/{template_name}".format(
            app_name=app_name,
            template_name=template_name
        )
        try:
            template = get_template(template_path)
        except TemplateDoesNotExist:
            raise Http404
        tpl_source = template.render(EMPTY_CONTEXT)

        if not request.META['HTTP_ACCEPT'].startswith('application/json'):
            return HttpResponse(tpl_source)
        return JsonResponse({'template': tpl_source})
