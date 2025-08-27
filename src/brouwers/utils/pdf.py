from django.template.response import TemplateResponse
from django.views.generic.base import TemplateResponseMixin, TemplateView


class PDFTemplateResponse(TemplateResponse):
    def __init__(self, filename=None, *args, **kwargs):
        kwargs["content_type"] = "application/pdf"
        super().__init__(*args, **kwargs)
        if filename:
            self["Content-Disposition"] = f'attachment; filename="{filename}"'
        else:
            self["Content-Disposition"] = "attachment"

    @property
    def rendered_content(self):
        """Returns the rendered pdf"""
        import weasyprint

        html = super().rendered_content
        base_url = self._request.build_absolute_uri("/")
        pdf = weasyprint.HTML(string=html, base_url=base_url).write_pdf()
        return pdf


class PDFTemplateResponseMixin(TemplateResponseMixin):
    response_class = PDFTemplateResponse
    filename = None

    def get_filename(self):
        """
        Returns the filename of the rendered PDF.
        """
        return self.filename

    def render_to_response(self, *args, **kwargs):
        """
        Returns a response, giving the filename parameter to PDFTemplateResponse.
        """
        kwargs["filename"] = self.get_filename()
        return super().render_to_response(*args, **kwargs)


class PDFTemplateView(TemplateView, PDFTemplateResponseMixin):
    pass
