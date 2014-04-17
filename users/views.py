from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy
from django.utils.http import base36_to_int
from django.utils.translation import ugettext as _
from django.views.generic import FormView, RedirectView

from forum_tools.forms import ForumUserForm
from general.forms import RedirectForm

from .tokens import activation_token_generator


User = get_user_model()


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'

    def get_form_kwargs(self):
        kwargs = super(LoginView, self).get_form_kwargs()
        kwargs.update(**{
            # 'request': self.request,
        })
        return kwargs

    def get_success_url(self):
        redirectform = RedirectForm(data=self.request.REQUEST)
        if redirectform.is_valid():
            next = redirectform.cleaned_data['redirect'] or redirectform.cleaned_data['next']
        else:
            next = settings.LOGIN_REDIRECT_URL
        return next

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
            'redirectform': RedirectForm(data=self.request.REQUEST),
        }
        context.update(**kwargs)
        return super(LoginView, self).get_context_data(**context)


class ActivationView(RedirectView):
    """ Check that a valid token is used and activate the user """
    url = reverse_lazy('profile')
    permanent = False

    def get(self, request, *args, **kwargs):
        """
        Check token raises a 403 if the token is invalid.
        """
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

        # backend attribute needed to log user in
        # NOTE: check safety options here
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(self.request, user)

        user.is_active = True
        user.save()
