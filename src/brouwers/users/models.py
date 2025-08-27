from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from brouwers.forum_tools.models import ForumUser
from brouwers.utils.storages import private_media_storage


class UserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not username:
            raise ValueError("The given username must be set")
        email = UserManager.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            is_staff=False,
            is_active=True,
            is_superuser=False,
            last_login=now,
            date_joined=now,
            **extra_fields,
        )

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

    def user_exists(self, username):
        qs = self.get_queryset().filter(username__iexact=username)
        return qs.exists()

    def get_from_forum(self, forum_user):
        try:
            return self.get(forumuser_id=forum_user.pk)
        except self.model.DoesNotExist:
            user = self.get(username=forum_user.username)
            user.forumuser_id = forum_user.pk
            user.save()
            return user
        raise self.model.DoesNotExist("Could not find system user for forum user")


class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username, password and email are required. Other fields are optional.
    """

    username = models.CharField(
        _("username"),
        max_length=30,
        unique=True,
        help_text=_("Required. 30 characters or fewer. All characters allowed."),
    )
    username_clean = models.CharField(_("cleaned username"), max_length=30, blank=True)
    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=30, blank=True)
    email = models.EmailField(_("email address"))
    phone = models.CharField(_("phone number"), max_length=15, blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as "
            "active. Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    ip_address_joined = models.GenericIPAddressField(
        _("ip address"),
        help_text=_("IP address used during registration."),
        protocol="both",
        blank=True,
        null=True,
    )

    # cross db-relation
    forumuser_id = models.IntegerField(_("forum user id"), blank=True, null=True)

    customer_group = models.ForeignKey(
        "shop.CustomerGroup",
        related_name=_("users"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ["username_clean"]

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.username:
            self.username_clean = self.username.lower()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        # TODO
        return f"/users/{self.id}/"

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name or self.username

    @cached_property
    def forumuser(self):
        if self.forumuser_id:
            forum_user = ForumUser.objects.filter(pk=self.forumuser_id).first()
        else:
            forum_user = ForumUser.objects.filter(username=self.username).first()
            if forum_user is not None:
                self.forumuser_id = forum_user.pk
                self.save()
        return forum_user

    @cached_property
    def profile(self):
        return self.userprofile


class DataDownloadRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    finished = models.DateTimeField(_("finished"), blank=True, null=True)
    downloaded = models.DateTimeField(_("downloaded"), blank=True, null=True)
    zip_file = models.FileField(
        _("zip file"), blank=True, storage=private_media_storage
    )

    def __str__(self):
        return _("Data download for {user} ({created})").format(
            user=self.user, created=self.created
        )
