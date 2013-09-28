from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render


from forms import RedirectForm


def custom_login(request):
    next_page = request.REQUEST.get('next')
    redirect_form = RedirectForm(request.REQUEST) #phpBB3 returns a 'redirect' key
    if redirect_form.is_valid():
        next_page = redirect_form.cleaned_data['redirect'] or next_page

    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            # Light security check -- make sure next_page isn't garbage.
            if not next_page or ' ' in next_page:
                next_page = settings.LOGIN_REDIRECT_URL
            
            user = form.get_user()
            login(request, user)
            return HttpResponseRedirect(next_page)
    else:
        form = AuthenticationForm(request)
    
    return render(request, 'general/login.html', {
        'form': form,
        'next': next_page,
        'redirect_form': redirect_form,
    })