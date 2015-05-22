from django.views.generic import TemplateView

from brouwers.utils.views import LoginRequiredMixin


class MyAlbumsView(LoginRequiredMixin, TemplateView):

    template_name = 'albums/my_albums.html'

    def get_public_albums(self):
        pass

    def get_private_albums(self):
        pass

    def get_shared_albums(self):
        pass
