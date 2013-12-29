from django import template

from ..models import Project

register = template.Library()

@register.filter(name='exclude_selected')
def filter_selected_projects(queryset, form):
    """Remove the selected projects in the voteform from the available projects"""
    if form.is_bound:
        for field in ('project1', 'project2', 'project3'):
            try:
                project = getattr(form.instance, field, None)
                if project:
                    queryset = queryset.exclude(id=project.id)
            except Project.DoesNotExist:
                continue
    return queryset