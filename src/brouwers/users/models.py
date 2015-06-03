from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from brouwers.forum_tools.models import ForumUser

from .mail import UserCreatedFromForumEmail


class UserManager(BaseUserManager):

    def create_user(self, username, email=None, password=None, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        email = UserManager.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=False, is_active=True, is_superuser=False,
                          last_login=now, date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        u = self.create_user(username, email, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u

    def create_from_forum(self, forum_user):
        extra_fields = {
            'forumuser_id': forum_user.user_id
        }
        user = self.create_user(forum_user.username, forum_user.user_email, **extra_fields)
        user.is_active = False
        user.save(using=self._db)

        # populate cache
        user.forumuser = forum_user
        # Send e-mail
        mail = UserCreatedFromForumEmail(**{'user': user})
        mail.send()
        return user

    def user_exists(self, username):
        qs = self.get_queryset().filter(username__iexact=username)
        return qs.exists()


class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username, password and email are required. Other fields are optional.
    """
    username = models.CharField(
        _('username'), max_length=30, unique=True,
        help_text=_('Required. 30 characters or fewer. All characters allowed.'))
    username_clean = models.CharField(_('cleaned username'), max_length=30, blank=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'))
    is_staff = models.BooleanField(
        _('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(
        _('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    # cross db-relation
    forumuser_id = models.IntegerField(_('forum user id'), blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['username_clean']

    def __unicode__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.username and not self.username_clean:
            self.username_clean = self.username.lower()
        super(User, self).save(*args, **kwargs)

    def get_absolute_url(self):
        # TODO
        return "/users/%d/" % self.id

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name or self.username

    @cached_property
    def forumuser(self):
        from django.db import DatabaseError
        try:
            return ForumUser.objects.get(pk=self.forumuser_id)
        except (ForumUser.DoesNotExist, DatabaseError):
            return None

    @cached_property
    def profile(self):
        return self.userprofile


# Circular imports happen otherwise
import signals  # noqa
