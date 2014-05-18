from .models import Preferences
from .utils import admin_mode


def user_is_album_admin(request):
    p = Preferences.get_or_create(request.user)

    is_album_admin = False
    try:
        if admin_mode(request.user, preferences=p):
            is_album_admin = True
    except TypeError: #anonymous user
        pass
    return {
        'user_is_album_admin': is_album_admin,
        'album_preferences': p
        }
