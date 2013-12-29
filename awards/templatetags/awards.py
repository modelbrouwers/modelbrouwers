from django import template

register = template.Library()

@register.filter(name='exclude_selected')
def filter_selected_projects(queryset, form):
    """Remove the selected projects in the voteform from the available projects"""
    if form.is_bound and getattr(form, 'cleaned_data', None):
        for field in ('project1', 'project2', 'project3'):
            project = form.cleaned_data.get(field, None)
            if project:
                queryset = queryset.exclude(id=project.id)
    return queryset