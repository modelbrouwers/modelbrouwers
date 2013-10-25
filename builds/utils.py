from .models import Build


def get_search_queryset(request, form=None, key='term'):
    # TODO: look into Haystack/Whoosh for relevance ordered results
    if form:
        search_term = form.cleaned_data['search_term']
    else:
        search_term = request.GET.get(key, '')
    
    qs = Build.objects.all()
    for term in search_term.split():
        qs = qs.filter(slug__icontains=term)
    return qs.select_related('user', 'profile', 'brand')