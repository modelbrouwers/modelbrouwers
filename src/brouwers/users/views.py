from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views import generic
from django.views.generic.detail import SingleObjectMixin

from django_sendfile import sendfile
from extra_views import InlineFormSetFactory, NamedFormsetsMixin, UpdateWithInlinesView

from brouwers.forum_tools.forms import ForumUserForm
from brouwers.general.forms import RedirectForm
from brouwers.general.models import UserProfile
from brouwers.general.utils import get_client_ip
from brouwers.utils.views import LoginRequiredMixin

from .forms import AuthForm, UserCreationForm
from .mail import UserRegistrationEmail
from .models import DataDownloadRequest

User = get_user_model()


class RedirectFormMixin:
    """Mixin to determine the next page after an authentication step."""

    default_redirect_url = settings.LOGIN_REDIRECT_URL
    permanent = False

    def _get_request_data(self):
        return self.request.POST if self.request.method == "POST" else self.request.GET

    def get_redirect_url(self):
        redirectform = RedirectForm(
            data=self._get_request_data(),
            request=self.request,
        )
        if redirectform.is_valid():
            return (
                redirectform.cleaned_data["redirect"]
                or redirectform.cleaned_data["next"]
            )
        if self.success_url:
            return super().get_redirect_url()
        return self.default_redirect_url


class LoginView(RedirectFormMixin, generic.FormView):
    form_class = AuthForm
    template_name = "users/login.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(dict(request=self.request))
        return kwargs

    def get_success_url(self):
        return self.get_redirect_url()

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        """Try and find existing users on the forum but not in the Django db"""
        forum_user_form = ForumUserForm(data=self.request.POST)
        if forum_user_form.is_valid():
            forum_user = forum_user_form.get_user()
            if forum_user is not None:
                return self.handle_forumuser(form, forum_user)
        return super().form_invalid(form)

    def handle_forumuser(self, form, forum_user):
        """Handle existing ForumUser's if the Django user wasn't found."""
        # Make sure no Django user exists!
        if User.objects.user_exists(forum_user.username):
            return super().form_invalid(form)

        # show message that the account was found,
        msg = _(
            "There is an existing forum account for this user. Please pick a different "
            "username."
        )
        messages.warning(self.request, msg)
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = {
            "redirectform": RedirectForm(
                data=self._get_request_data(), request=self.request
            ),
        }
        context.update(**kwargs)
        return super().get_context_data(**context)


class LogoutView(RedirectFormMixin, generic.RedirectView):
    default_redirect_url = "/"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            msg = _("You have been logged out.")
        else:
            msg = _("Can't log you out, you weren't logged in!")
        messages.info(request, msg)
        return super().get(request, *args, **kwargs)


class RegistrationView(RedirectFormMixin, generic.CreateView):
    model = User
    form_class = UserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:profile")

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("index")
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        assert user is not None
        user.ip_address_joined = get_client_ip(self.request)
        user.save()
        self.do_login(form)

        mail = UserRegistrationEmail(user=self.object)
        transaction.on_commit(mail.send)
        return response

    def do_login(self, form):
        pw = form.cleaned_data["password1"]
        user = authenticate(username=self.object.username, password=pw)
        login(self.request, user)


class ProfileInline(InlineFormSetFactory):
    model = UserProfile
    fields = (
        "street",
        "number",
        "postal",
        "city",
        "province",
        "country",  # address
        "exclude_from_nomination",  # awards
    )
    factory_kwargs = {
        "can_delete": False,
        "extra": 0,
        "max_num": 1,
    }


class ProfileView(LoginRequiredMixin, NamedFormsetsMixin, UpdateWithInlinesView):
    model = User
    fields = ("first_name", "last_name", "email")
    template_name = "users/profile_edit.html"

    inlines = [ProfileInline]
    inlines_names = ["profiles"]

    def get_object(self):
        return self.request.user

    def forms_valid(self, form, inlines):
        response = super().forms_valid(form, inlines)
        messages.success(self.request, _("Your profile data has been updated."))
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pw_form"] = PasswordChangeForm(self.request.user)
        return context


class UserProfileDetailView(LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = "users/profile.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["albums"] = (
            self.object.album_set.select_related("cover")
            .filter(trash=False, public=True)
            .order_by("title")
        )
        return ctx


class PasswordChangedView(generic.RedirectView):
    pattern_name = "users:profile"
    permanent = False

    def get(self, request, *args, **kwargs):
        messages.success(request, _("Your password was changed."))
        return super().get(request, *args, **kwargs)


class RequestDataDownloadView(LoginRequiredMixin, generic.View):
    raise_exception = True

    def post(self, *args, **kwargs):
        if not DataDownloadRequest.objects.filter(
            user=self.request.user, finished__isnull=True
        ).exists():
            DataDownloadRequest.objects.create(user=self.request.user)
        messages.success(
            self.request,
            _(
                "Your data download is being prepared and will be e-mailed when it's ready!"
            ),
        )
        return redirect(reverse("users:profile"))


class DataDownloadFileView(LoginRequiredMixin, SingleObjectMixin, generic.View):
    def get_queryset(self):
        qs = DataDownloadRequest.objects.filter(
            user=self.request.user, finished__isnull=False
        ).exclude(zip_file="")
        return qs

    def get(self, request, *args, **kwargs):
        download_request = self.get_object()
        download_request.downloaded = timezone.now()
        download_request.save(update_fields=["downloaded"])
        zip_file = download_request.zip_file
        return sendfile(request, zip_file.path, attachment=True)
