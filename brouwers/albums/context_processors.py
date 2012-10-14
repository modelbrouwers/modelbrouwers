from models import Preferences
from utils import admin_mode
from django.db import connection as _connection

def preferences(request):
    try:
        p = Preferences.get_or_create(request.user)
    except TypeError: #anonymous user
        p = Preferences()
    return {'album_preferences': p}

def user_is_album_admin(request):
    is_album_admin = False
    try:
        if admin_mode(request.user):
            is_album_admin = True
    except TypeError: #anonymous user
        pass
    return {'user_is_album_admin': is_album_admin}

def connection(request):
    return {'connection': _connection}
