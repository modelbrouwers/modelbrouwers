from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render


from forms import *
from models import KitReview


def index(request):
    reviews = KitReview.objects.all()
    return render(request, 'kitreviews/base.html', {'reviews': reviews})


@login_required
def add_review(request):
    if request.method == 'POST':
        kitform = ModelKitForm(request.POST, prefix='kit')
        reviewform = KitReviewForm(request.user, request.POST, prefix='review')
    else:
        kitform = ModelKitForm(prefix='kit')
        reviewform = KitReviewForm(request.user, prefix='review')

    return render(request, 'kitreviews/add_review.html', {
            'kitform': kitform,
            'reviewform': reviewform,
        })

def find_kit(request):
    kitform, results = FindModelKitForm(request.GET), None
    if kitform.is_valid() and 'brand' in request.GET:
        results = ModelKit.objects.all().select_related(
            'brand', 'scale', 'category')

        brand = kitform.cleaned_data['brand']
        if brand:
            results = results.filter(brand_id=brand.id)

        kit_number = kitform.cleaned_data['kit_number']
        if kit_number:
            results = results.filter(kit_number__icontains=kit_number)

        kit_name = kitform.cleaned_data['kit_name']
        if kit_name:
            name_parts = kit_name.split(' ')
            # order doesn't matter, just find the kits with names that have all
            # the search terms
            q_list = []
            for part in name_parts:
                q_list.append(Q(kit_name__icontains=part))
            results = results.filter(*q_list)

        scale = kitform.cleaned_data['scale']
        if scale:
            results = results.filter(scale_id=scale.id)

        category = kitform.cleaned_data['category']
        if category:
            results = results.filter(category_id=category.id)


    # import pdb; pdb.set_trace()

    return render(request, 'kitreviews/find_kit.html', {
            'kitform': kitform,
            'kits': results,
        })