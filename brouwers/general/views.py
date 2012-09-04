from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives, send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.core.validators import validate_email
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.hashcompat import sha_constructor
from django.utils.safestring import mark_safe

from brouwers.albums.models import Album
from brouwers.albums.utils import admin_mode
from brouwers.awards.models import Project
from brouwers.secret_santa.models import Participant

from forms import *
from models import UserProfile
from shortcuts import render_to_response
from datetime import date
from django.conf import settings

try:
    from brouwers.migration.models import UserMigration
except ImportError:
    UserMigration = None

def index(request):
    if not request.user.has_perm('albums.access_albums'):
        return HttpResponseRedirect('/index.php') #to old albums
    return render_to_response(request, 'base.html')

### ready for implementation on modelbrouwers.nl
def register(request):
    if request.method=='POST':
        #form = UserProfileForm(request.POST)
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = user.username
            nickname = form.cleaned_data['forum_nickname']
            password = form.cleaned_data['password1']
            new_user = authenticate(username = username, password = password)
            login(request, new_user)
            
            subject = 'Registratie op xbbtx.be'
            message = 'Bedankt voor uw registratie op http://xbbtx.be.\n\nU hebt geregistreerd met de volgende gegevens:\n\nGebruikersnaam: %s\nWachtwoord: %s\n\nBewaar deze gegevens voor als u uw login en/of wachtwoord mocht vergeten.' % (nickname, password)
            sender = 'sergeimaertens@skynet.be'
            receiver = [form.cleaned_data['email']]
            send_mail(subject, message, sender, receiver, fail_silently=True)      
            
            next_page = request.GET.get('next', reverse(profile))
            if ' ' in next_page:
            	next_page = reverse(profile)
            return HttpResponseRedirect(next_page)
    else:
        form = RegistrationForm()
    return render_to_response(request, 'general/register.html', {'form': form})

### almost ready for implementation on modelbrouwers.nl
def custom_login(request):    
    next_page = request.REQUEST.get('next')
    if request.method == "POST":
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            # Light security check -- make sure next_page isn't garbage.
            if not next_page or ' ' in next_page:
                next_page = settings.LOGIN_REDIRECT_URL
            
            user = form.get_user()
            login(request, user)
            return HttpResponseRedirect(next_page)
        else: 
            #ok, maybe an existing forumuser trying to login, but the accounts aren't coupled yet
            username = request.POST['username']
            users = User.objects.filter(username__iexact = username)
            if UserMigration:
                try:
                    migration_user = UserMigration.objects.get(username=username)
                    if not users: #user exists on the forum, but not in our db
                        # save user, set user inactive and generate + send the key
                        username_ = username.replace(" ", "_")
                        email = migration_user.email
                        password = User.objects.make_random_password(length=8)
                        
                        #set the password later, when validating the hash
                        user = User.objects.create_user(username_, email, password)
                        user.is_active = False
                        user.save()
                        profile = UserProfile(user=user, forum_nickname=username)
                        profile.save()
                        
                        #ok, user created, now compose email etc.
                        h = sha_constructor(settings.SECRET_KEY + username).hexdigest()[:24]
                        migration_user.hash = h
                        migration_user.save()
                        domain = Site.objects.get_current().domain
                        
                        url = "http://%s%s"% (domain, reverse(confirm_account))
                        url_a = "<a href=\"%s\">%s</a>" % (url, url)
                        text_content = "Beste %s,\n\nUw code is: %s.\nGeef deze code in op: %s\n\nMvg,\nHet beheer" % (username, h, url)
                        html_content = "<p>Beste %s,</p><br >" % username
                        html_content += "<p>Uw code is: <strong>%s</strong>.</p>" % h
                        html_content += "<p>Geef deze code in op: %s</p><br >" % url_a
                        html_content += "<p>Mvg,</p><p>Het beheer</p>"
                        subject, from_email = 'Modelbrouwersaccount', 'beheer@modelbrouwers.nl'
                        
                        msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
                        msg.attach_alternative(html_content, "text/html")
                        msg.send()
                        #send_mail(subject, mailtext, from_email, [to], fail_silently=True)
                        return render_to_response(request, 'general/user_migration.html', {'username': username})
                except UserMigration.DoesNotExist: #unknown on the forum
                    pass  
    else:
        form = AuthenticationForm(request)
    return render_to_response(request, 'general/login.html', {
        'form': form,
        'next': next_page,
    })
  
def custom_logout(request):
    next_page = request.GET.get('next')
    if not next_page or ' ' in next_page:
        next_page = "/?logout=1"
    logout(request)
    return HttpResponseRedirect(next_page)

def confirm_account(request):
    if request.method == "POST":
        # takes the forumnickname, two password fields and the hash
        form = ForumAccountForm(request.POST)
        if form.is_valid():
            nickname = form.cleaned_data["forum_nickname"]
            username_ = nickname.replace(" ", "_")
            user = get_object_or_404(User, username=username_, is_active=False)
            user.is_active = True
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()
            
            #logging in
            user = authenticate(username=username_, password=password)
            login(request, user)
            return HttpResponseRedirect('/phpBB3/')
    else:
        form = ForumAccountForm()
    return render_to_response(request, 'general/confirm_account.html', {'form': form})

#############################
#    showing userprofile    #
#############################

@user_passes_test(lambda u: u.is_authenticated(), login_url='/login/')
def profile(request):
    forms = {}
    if request.method=='POST':
        forms['profileform'] = ProfileForm(request.POST, instance=request.user.get_profile())
        forms['userform'] = UserForm(request.POST, instance=request.user)
        
        if forms['profileform'].is_valid():
            forms['profileform'].save()
            if forms['profileform'].cleaned_data['exclude_from_nomination']==True:
                projects = Project.objects.filter(brouwer__iexact=request.user.get_profile().forum_nickname)
                for project in projects:
                    project.rejected = True
                    project.save()
            if forms['profileform'].cleaned_data['secret_santa']==True:
                participants = Participant.objects.filter(Q(user__exact=request.user) & Q(year=date.today().year))
                if not participants:
                    participant = Participant(user=request.user, year=date.today().year)
                    participant.save()
            if forms['profileform'].cleaned_data['secret_santa']==False:
                participants = Participant.objects.filter(Q(user__exact=request.user) & Q(year=date.today().year))
                if participants:
                    participants[0].delete()

        if forms['userform'].is_valid():
            forms['userform'].save()
        return render_to_response(request, 'general/profile.html', forms)
    else:
        forms['profileform'] = ProfileForm(instance=request.user.get_profile())
        forms['userform'] = UserForm(instance=request.user)
        return render_to_response(request, 'general/profile.html', forms)

def user_profile(request, username=None):
    profile = get_object_or_404(UserProfile, user__username=username)
    q = Q(trash=False, user=profile.user)
    if request.user.is_authenticated():
        if not admin_mode(request.user):
            q = Q(q, public=True)
    albums = Album.objects.filter(q)
    total = albums.count()
    
    p = Paginator(albums, 24)
    page = request.GET.get('page', 1)
    try:
        albums = p.page(page)
    except (PageNotAnInteger, TypeError):
        # If page is not an integer, deliver first page.
        albums = p.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        albums = p.page(p.num_pages)
    
    needs_closing_tag_row_albums = False
    if len(albums) % 4 != 0:
        needs_closing_tag_row_albums = True
    return render_to_response(request, 'general/public_profile.html', 
        {
            'profile': profile, 
            'albums': albums, 
            'page': 'page', 
            'objects': albums, 
            'needs_closing_tag_row': needs_closing_tag_row_albums,
            'total': total,
        }
    )
