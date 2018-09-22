import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Q

logger = logging.getLogger(__name__)


class EmailModelBackend(ModelBackend):
    """
    Authenticates against settings.AUTH_USER_MODEL, but also
    looks at the e-mailaddress of the user and the case-insensitive username.
    """

    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        try:
            user = UserModel._default_manager.get(
                Q(username__iexact=username) | Q(email=username)
            )
        except UserModel.DoesNotExist:
            return None
        except MultipleObjectsReturned:
            logger.error("Multiple case-insensitive usernames matched! Username: %s", username)
            return None

        if user.check_password(password):
            return user

        return None
