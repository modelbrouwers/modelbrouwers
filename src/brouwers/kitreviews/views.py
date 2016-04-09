from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from forms import *
from models import *


def index(request):
    reviews = KitReview.objects.all()
    return render(request, 'kitreviews/base.html', {'reviews': reviews})


class AddReview(CreateView):
    model = KitReview
    template_name = 'kitreviews/add_review.html'
    form_class = KitReviewForm


class FindKit(DetailView):
    pass


class KitDetail(DetailView):
    pass
