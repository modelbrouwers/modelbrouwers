from django.contrib.auth.decorators import login_required
from django.shortcuts import render


from forms import *
from models import KitReview


def index(request):
    reviews = KitReview.objects.all()
    return render(request, 'kitreviews/base.html', {'reviews': reviews})


@login_required
def add_review(request):
    if request.method == 'POST':
        reviewform = KitReviewForm(request.user, request.POST)
        if reviewform.is_valid():
            print 'ok'
    else:
        kitform = ModelKitForm()
        reviewform = KitReviewForm(request.user)

    return render(request, 'kitreviews/add_review.html', {
            'kitform': kitform,
            'reviewform': reviewform,
        })
