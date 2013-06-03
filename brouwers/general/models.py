from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from datetime import date, datetime

from awards.models import Category
from utils import get_client_ip, lookup_http_blacklist

COUNTRY_CHOICES = (
    ("N",_("The Netherlands")),
    ("B",_("Belgium")),
    ("D",_("Germany")),
    ("F",_("France")),
)

class OrderedUser(User):
    class Meta:
        ordering = ["username"]
        proxy = True
    
    def __unicode__(self):
        return u"%s" % self.username.replace('_', ' ')

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    #awardsinfo  
    last_vote = models.DateField(default=date(2010,1,1))
    forum_nickname = models.CharField(max_length=30, unique=True)
    exclude_from_nomination = models.BooleanField(_("exclude me from nominations"), help_text=_("If checked, you will be excluded from Awards-nominations."))
    categories_voted = models.ManyToManyField(Category, blank=True, null=True)
    
    secret_santa = models.BooleanField(help_text=_("Aanvinken als je meedoet")) # No longer used TODO remove
    #adres
    street = models.CharField(_("street name"), max_length=255, blank=True, null=True)
    number = models.CharField(
            _("number"), max_length=10, 
            help_text=_("house number (+ PO box if applicable)"), 
            blank=True, null=True
        )
    postal = models.CharField(_("postal code"), max_length=10, blank=True, null=True)
    city = models.CharField(_("city"), max_length=255, blank=True, null=True)
    province = models.CharField(_("province"), max_length=255, blank=True, null=True)
    country = models.CharField(_("country"), max_length=1, choices=COUNTRY_CHOICES, blank=True, null=True)
    
    #voorkeuren -> TODO: move to secret santa object
    preference = models.TextField(help_text=_("Dit wil ik graag"), blank=True, null=True)
    refuse = models.TextField(help_text=_("Dit wil ik absoluut niet"), blank=True, null=True)

    # allow social sharing
    allow_sharing = models.BooleanField(_("allow social sharing"), default=True, 
            help_text=_('Checking this gives us permission to share your topics and albums on social media. Uncheck if you don\'t want to share.')
        )
    
    def __unicode__(self):
        return u"%s" % self.forum_nickname
    
    def full_name(self):
        return self.user.get_full_name()
    
    class Meta:
        verbose_name = _("userprofile")
        verbose_name_plural = _("userprofiles")
        ordering = ['forum_nickname']
    
    @property
    def is_address_ok(self):
        ok = False
        if self.street and self.number and self.postal and self.city and self.country:
            ok = True
        return ok

class QuestionAnswer(models.Model):
    answer = models.CharField(max_length=255)
    
    def __unicode__(self):
        return u"%s" % self.answer
    
class RegistrationQuestion(models.Model):
    question = models.CharField(max_length=255, help_text=_("Question which must be answered for registration."))
    answers = models.ManyToManyField(QuestionAnswer, blank=True, null=True)
    in_use = models.BooleanField(default=True)
    
    def __unicode__(self):
        return u"%s" % self.question

class RegistrationAttempt(models.Model):
    username = models.CharField(_('username'), max_length=512, db_index=True) # same as forum_nickname
    question = models.ForeignKey(RegistrationQuestion, verbose_name=_('registration question'))
    answer = models.CharField(_('answer'), max_length=255)
    # answer_correct = models.BooleanField(_('correct answer?'))
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)
    ip_address = models.IPAddressField(_('IP address'), db_index=True)
    success = models.BooleanField(_('success'))
    
    # keeping spam out
    potential_spammer = False
    type_of_visitor = models.CharField(_('type of visitor'), max_length=255, default=_('normal user'))
    
    class Meta:
        verbose_name = _('registration attempt')
        verbose_name_plural = _('registration attempts')
        ordering = ('-timestamp',)
    
    def __unicode__(self):
        return u"%s" % self.username
    
    @classmethod
    def add(cls, request):
        ip = get_client_ip(request)
        instance = cls(
            username = request.POST.get('forum_nickname'),
            question_id = request.POST.get('question'),
            answer = request.POST.get('answer'),
            ip_address = ip
            )
        
        type_of_visitor, potential_spammer = lookup_http_blacklist(ip)
        if type_of_visitor is not None and potential_spammer is not None:
            instance.potential_spammer = potential_spammer
            instance.type_of_visitor = type_of_visitor
        
        instance.save()
        return instance

class SoftwareVersion(models.Model):
    VERSION_TYPES = (
        ('a', 'alpha'),
        ('b', 'beta'),
        ('v', 'vanilla')
    )
    state = models.CharField(max_length=1, choices=VERSION_TYPES, default='v')
    major = models.PositiveSmallIntegerField(default=1)
    minor = models.PositiveSmallIntegerField(default=0)
    detail = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    start = models.DateTimeField(default=datetime.now)
    end = models.DateTimeField(default=datetime.now)
    changelog = models.TextField(blank=True)
    
    class Meta:
        ordering = ('-state', '-major', '-minor', '-detail')
    
    def __unicode__(self):
        prefix = ''
        if self.state != 'v':
            prefix = '%s-' % self.get_state_display()
        detail = '.' + str(self.detail) or ''
        return u"%s%s.%s%s" % (prefix, self.major, self.minor, detail)

class PasswordReset(models.Model):
    user = models.ForeignKey(User)
    h = models.CharField(_("hash"), max_length=256)
    expire = models.DateTimeField(_("expire datetime"))
    
    class Meta:
        verbose_name = _("password reset")
        verbose_name_plural = _("password resets")
        ordering = ('expire',)
        unique_together = (('user', 'h'),)
    
    def __unicode__(self):
        return _("Password reset for %(user)s") % {'user': self.user.get_profile().__unicode__()}

class Redirect(models.Model):
    path_from = models.CharField(
            _("path from"), 
            max_length=255, 
            help_text=_("path from where to redirect, without leading slash. \
                        E.g. '/shop/' becomse 'shop/'."),
            unique=True
            )
    path_to = models.CharField(_("redirect to"), max_length=1024,
            help_text=_("Path (relative or absolute to the docroot) or url.")
    )
   
    class Meta:
        verbose_name = _("redirect")
        verbose_name_plural = _("redirects")
        ordering = ('path_from',)
    
    def __unicode__(self):
        return u"%s" % self.path_from
