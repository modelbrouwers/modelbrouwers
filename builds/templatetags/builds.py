from django import template

register = template.Library()

@register.filter
def can_edit(build, user):
    try:
        if user.has_perm('builds.edit_build') or build.user_id == user.id:
            return True
    except:
        pass
    return False