import json
from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin

from .models import Photo
from .utils import admin_mode


# CLASS BASED VIEWS ###

class RotateView(SingleObjectMixin, View):
    """ View taking a photo, rotating it, and returning the success status when done """
    model = Photo

    def get_queryset(self):
        qs = super(RotateView, self).get_queryset()
        if not admin_mode(self.request.user):
            qs = qs.filter(user=self.request.user)
        return qs

    def post(self, request, *args, **kwargs):
        photo = self.get_object()
        direction = self.request.POST['direction']
        if direction == 'cw':
            photo.rotate_right()
        elif direction == 'ccw':
            photo.rotate_left()
        else:
            response = {'result': 'Invalid direction'}

        response = {'result': 'success', 'ok': True}
        return HttpResponse(json.dumps(response), content_type='application/json')
