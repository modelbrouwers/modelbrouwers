from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import MultipleObjectsReturned


class EmailModelBackend(ModelBackend):
    """
    Authenticates against settings.AUTH_USER_MODEL, but also
    looks at the e-mailaddress of the user.
    """

    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel._default_manager.get(email=username)
            if user.check_password(password):
                return user
        # Legacy e-mailadresses can be non-unique, fix later
        except (UserModel.DoesNotExist, MultipleObjectsReturned):
            return None
