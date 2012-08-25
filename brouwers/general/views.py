from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.validators import validate_email
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.hashcompat import sha_constructor

from brouwers.albums.models import Album
from brouwers.awards.models import Project
from brouwers.secret_santa.models import Participant

from forms import *
from models import UserProfile
from shortcuts import render_to_response
from datetime import date
import settings

try:
    from brouwers.migration.models import UserMigration
except ImportError:
    UserMigration = None

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
            
            return HttpResponseRedirect('/profile/')
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
                migration_user = UserMigration.objects.get(username=username)
                if migration_user and not users: #user exists on the forum, but not in our db
                    # save user, set user inactive and generate + send the key
                    username_ = username.replace(" ", "_")
                    email = migration_user.email
                    password = User.objects.make_random_password(length=8)
                    password = 'test' #TODO: remove me
                    #set the password later, when validating the hash
                    user = User.objects.create_user(username_, email, password)
                    user.is_active = False
                    user.save()
                    #ok, user created, now compose email etc.
                    h = sha_constructor(settings.SECRET_KEY + username).hexdigest()[:24]
                    migration_user.hash = h
                    migration_user.save()
                    text = "Beste %s,\nOp Modelbrouwers.nl proberen we het gebruiksgemak zo hoog mogelijk te houden. In het kader daarvan stappen we over op een overkoepelende Modelbrouwers.nl account. U bent een bestaande forumgebruiker, maar uw overkoepelende account werd net aangemaakt. Om uw identiteit tijdens deze koppeling te controleren, hebben wij eenmalig een code naar uw e-mailadres gestuurd. In de e-mail vindt u ook een link waar u die code kan ingeven. Deze koppeling is een eenmalige gebeurtenis."
                    url = 'http://xbbtx.be/validate_code/'
                    mailtext = "Beste %s,\n\nUw code is: %s. Geef deze code in op: %s\n\nMvg,\nHet beheer" % (username, h, url)
                    subject = 'Modelbrouwersaccount'
                    send_mail(subject, mailtext, 'beheer@modelbrouwers.nl', [email], fail_silently=True)
                    return render_to_response(request, 'general/user_migration.html', {'username': username})
                
    else:
        form = AuthenticationForm(request)
    return render_to_response(request, 'general/login.html', {
        'form': form,
        'next': next_page,
    })

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
        
def custom_logout(request):
    next_page = request.GET.get('next')
    if not next_page or ' ' in next_page:
        next_page = "/?logout=1"
    logout(request)
    return HttpResponseRedirect(next_page)


#############################
#    showing userprofile    #
#############################

def user_profile(request, username=None):
    profile = get_object_or_404(UserProfile, user__username=username)
    albums = Album.objects.filter(trash=False, user=profile.user, public=True)
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
