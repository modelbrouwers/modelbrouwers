from django.core.mail import EmailMultiAlternatives, send_mail
from django.shortcuts import get_object_or_404
from datetime import date

def get_current_ss(ss_class):
    today = date.today()
    this_year = today.year
    if today.month in [1,2]:
        this_year -= 1
    secret_santa = get_object_or_404(ss_class, year=this_year)
    return secret_santa

MAIL_TEMPLATE_PLAIN = """
Hallo %(sender)s,

De lootjesverdeling van de Secret Santa %(ss_year)s is weer gebeurd! Hieronder vind je de gegevens van jouw lootje.

Naam: %(full_name)s (%(forum_name)s)
Adres: %(street)s %(number)s
%(postal)s %(city)s
%(province)s
%(country)s

Je kan deze gegevens en de voorkeuren van jouw lootje bekijken op http://modelbrouwers.nl/secret_santa/receiver/.

Mvg,
Het beheer
"""

def do_lottery_mailing(couples):
    ss = couples[0].secret_santa
    for couple in couples:
        profile = couple.receiver.user.get_profile()
        subject, sender = 'Secret Santa', 'admins@modelbrouwers.nl'
        receivers = [couple.sender.user.email]
        message = MAIL_TEMPLATE_PLAIN % {
            'sender': couple.sender.__unicode__(),
            'ss_year': ss.year,
            'full_name': couple.receiver.user.get_full_name(),
            'forum_name': couple.receiver.__unicode__(),
            'street': profile.street,
            'number': profile.number,
            'postal': profile.postal,
            'city': profile.city,
            'province': profile.province,
            'country': profile.get_country_display(),
        }
        send_mail(subject, message, sender, receivers, fail_silently=True)  
    return None
