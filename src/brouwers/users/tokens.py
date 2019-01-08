from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from django.utils.crypto import constant_time_compare, salted_hmac
from django.utils.http import base36_to_int, int_to_base36


class ActivationTokenGenerator(PasswordResetTokenGenerator):
    """
    Strategy object used to generate and check tokens for the
    user activation mechanism.
    """

    def make_token(self, user):
        key_salt = 'brouwers.users.tokens.ActivationTokenGenerator'
        user_info = int(user.is_active) + user.id + user.forumuser_id
        user_info_b36 = int_to_base36(user_info)

        # user.is_active makes it a one time use only
        value = (six.text_type(user.pk) + user.password +
                 six.text_type(user.is_active))
        hash = salted_hmac(key_salt, value).hexdigest()[::2]
        return "%s-%s" % (user_info_b36, hash)

    def check_token(self, user, token):
        """ Check that the activation token is correct for a given user """
        try:
            user_info_b36, hash = token.split("-")
        except ValueError:
            return False

        try:
            base36_to_int(user_info_b36)
        except ValueError:
            return False

        # check that the user_info/uid has not been tampered with
        # and that the user is still inactive
        if not constant_time_compare(self.make_token(user), token):
            return False
        return True


activation_token_generator = ActivationTokenGenerator()
