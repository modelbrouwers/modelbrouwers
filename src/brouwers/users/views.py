from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.utils.http import base36_to_int
from django.utils.translation import ugettext as _
from django.views import generic

from extra_views import UpdateWithInlinesView, NamedFormsetsMixin, InlineFormSet

from brouwers.forum_tools.forms import ForumUserForm
from brouwers.general.forms import RedirectForm
from brouwers.general.models import RegistrationQuestion, RegistrationAttempt, UserProfile
from brouwers.utils.views import LoginRequiredMixin
from .forms import UserCreationForm
from .mail import UserRegistrationEmail
from .tokens import activation_token_generator

User = get_user_model()


class RedirectFormMixin(object):
    """ Mixin to determine the next page after an authentication step. """
    default_redirect_url = settings.LOGIN_REDIRECT_URL
    permanent = False

    def _get_request_data(self):
        return self.request.POST if self.request.method == 'POST' else self.request.GET

    def get_redirect_url(self):
        redirectform = RedirectForm(data=self._get_request_data())
        if redirectform.is_valid():
            return redirectform.cleaned_data['redirect'] or redirectform.cleaned_data['next']
        if self.success_url:
            return super(RedirectFormMixin, self).get_redirect_url()
        return self.default_redirect_url


class LoginView(RedirectFormMixin, generic.FormView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'

    def get_form_kwargs(self):
        kwargs = super(LoginView, self).get_form_kwargs()
        kwargs.update(dict(request=self.request))
        return kwargs

    def get_success_url(self):
        return self.get_redirect_url()

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super(LoginView, self).form_valid(form)

    def form_invalid(self, form):
        """ Try and find existing users on the forum but not in the Django db """
        forum_user_form = ForumUserForm(data=self.request.POST)
        if forum_user_form.is_valid():
            forum_user = forum_user_form.get_user()
            if forum_user is not None:
                return self.handle_forumuser(form, forum_user)
        return super(LoginView, self).form_invalid(form)

    def handle_forumuser(self, form, forum_user):
        """ Handle existing ForumUser's if the Django user wasn't found. """
        # Make sure no Django user exists!
        if User.objects.user_exists(forum_user.username):
            return super(LoginView, self).form_invalid(form)

        # create an inactive Django user, this also sends the e-mail!
        User.objects.create_from_forum(forum_user)

        # show message that the account was found, but is inactive
        msg = _('We found an existing forum account for this username, '
                'but it appears that were was no coupling account yet. '
                'We automatically created a coupling account, which is '
                'not activated yet. You should receive an e-mail soon '
                'with a link to activate your account. '
                'Coupling accounts were added to introduce SSO (single '
                'sign on) in the future for the entire domain.'
                )
        messages.warning(self.request, msg)
        context = self.get_context_data(**{'forum_user': forum_user})
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = {
            'redirectform': RedirectForm(data=self._get_request_data()),
        }
        context.update(**kwargs)
        return super(LoginView, self).get_context_data(**context)


class LogoutView(RedirectFormMixin, generic.RedirectView):
    default_redirect_url = '/'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            logout(request)
            msg = _('You have been logged out.')
        else:
            msg = _('Can\'t log you out, you weren\'t logged in!')
        messages.info(request, msg)
        return super(LogoutView, self).get(request, *args, **kwargs)


class ActivationView(generic.RedirectView):
    """ Check that a valid token is used and activate the user """
    url = reverse_lazy('users:profile')
    permanent = False

    def get(self, request, *args, **kwargs):
        """ Check token raises a 403 if the token is invalid. """
        self.check_token()
        return super(ActivationView, self).get(request, *args, **kwargs)

    def check_token(self):
        uidb36 = self.kwargs.get('uidb36')
        token = self.kwargs.get('token')
        assert uidb36 is not None and token is not None
        user_id = base36_to_int(uidb36)
        user = User._default_manager.get(pk=user_id)

        valid = activation_token_generator.check_token(user, token)
        if not valid:
            raise PermissionDenied

        user.is_active = True
        user.save()
        # backend attribute needed to log user in
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(self.request, user)


class RegistrationView(RedirectFormMixin, generic.CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:profile')
    registration_attempt = None

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('index')
        return super(RegistrationView, self).get(request, *args, **kwargs)

    def get_initial(self):
        initial = super(RegistrationView, self).get_initial()
        initial['question'] = RegistrationQuestion.active.all().order_by('?')[0]
        return initial

    def log_registration(self, form):
        if settings.LOG_REGISTRATION_ATTEMPTS:
            self.registration_attempt = RegistrationAttempt.objects.create_from_form(self.request, form.cleaned_data)

    def form_invalid(self, form):
        """ Log the registration attempts before handling the form """
        rest_valid = set(form.errors.keys()).issubset(set(['question', 'answer', '__all__']))
        if (form.errors.get('answer') or form.errors.get('question')) and rest_valid:
            self.log_registration(form)
        if self.registration_attempt:
            self.registration_attempt.set_ban()  # FIXME
        return super(RegistrationView, self).form_invalid(form)

    def form_valid(self, form):
        """
        If the user is consider trustworthy, log him/her in. Else,
        make the account inactive and send an e-mail to the admins.
        """
        self.log_registration(form)
        response = super(RegistrationView, self).form_valid(form)

        mail = UserRegistrationEmail(user=self.object)
        mail.send()

        if self.registration_attempt:
            # possible spammer: log attemt, send e-mail
            if self.registration_attempt.potential_spammer:
                self.object.is_active = False
                self.object.save()
                # TODO: e-mail send_inactive_user_mail(new_user), template is in general app
            else:
                self.do_login(form)
                self.registration_attempt.success = True
                self.registration_attempt.save()
        else:
            self.do_login(form)
        return response

    def do_login(self, form):
        pw = form.cleaned_data['password1']
        user = authenticate(username=self.object.username, password=pw)
        login(self.request, user)


class ProfileInline(InlineFormSet):
    model = UserProfile
    fields = (
        'street', 'number', 'postal', 'city', 'province', 'country',  # address
        'exclude_from_nomination',  # awards
        'allow_sharing',  # privacy
    )
    can_delete = False
    extra = 0
    max_num = 1


class ProfileView(LoginRequiredMixin, NamedFormsetsMixin, UpdateWithInlinesView):
    model = User
    fields = ('first_name', 'last_name', 'email')
    template_name = 'users/profile_edit.html'

    inlines = [ProfileInline]
    inlines_names = ['profiles']

    def get_object(self):
        return self.request.user

    def forms_valid(self, form, inlines):
        response = super(ProfileView, self).forms_valid(form, inlines)
        messages.success(self.request, _('Your profile data has been updated.'))
        return response

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['pw_form'] = PasswordChangeForm(self.request.user)
        return context


class UserProfileDetailView(LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        ctx = super(UserProfileDetailView, self).get_context_data(**kwargs)
        ctx['albums'] = self.object.album_set.select_related('cover').filter(
            trash=False, public=True).order_by('title')
        return ctx


class PasswordChangedView(generic.RedirectView):
    pattern_name = 'users:profile'
    permanent = False

    def get(self, request, *args, **kwargs):
        messages.success(request, _('Your password was changed.'))
        return super(PasswordChangedView, self).get(request, *args, **kwargs)
