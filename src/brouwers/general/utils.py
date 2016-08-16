# -*- coding: UTF-8 -*-

import socket

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import Context, loader


def get_forumname_for_username(username):
    return username.replace("_", " ")  # FIXME NOT always valid, users can have underscores!


def get_username_for_user(user):
    return get_forumname_for_username(user.username)


def get_username(obj, field='user'):
    user = getattr(obj, field)
    username = get_username_for_user(user)
    return username


def clean_username(username):
    return username.replace(u"'", u'ʹ').lower()


def clean_username_fallback(username):
    return username.replace('\'', ' ').lower()


# KEEPING SPAMMERS OUT ####################
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')


BLOCKING_LEVELS = {
    u'1': u'suspicious',
    u'2': u'harvester',
    u'3': u'suspicious & harvester',
    u'4': u'comment spammer',
    u'5': u'suspicious & comment spammer',
    u'6': u'harvester & comment spammer',
    u'7': u'suspicious & harvester & comment spammer'
}


def lookup_http_blacklist(ip):
    """ Checks if an ip is a potential spammer.

        Returns a tupple (type_of_visitor, potential_spammer), e.g. ('comment spammer', True)
    """
    return (None, None)  # disable lookups for now, not thread safe, TODO: celery
    # FIXME

    if settings.DEVELOPMENT:
        ip = '220.249.167.159'
    key = settings.HTTPBL_ACCESS_KEY
    octets = ip.split('.')
    octets.reverse()
    reverse_ip = '.'.join(octets)

    host = u"%s.%s.dnsbl.httpbl.org" % (key, reverse_ip)
    result = socket.getaddrinfo(host, 80)

    # go with the first hit
    ip = result[0][4][0]
    octets = ip.split('.')
    if octets[0] == '127':
        # format is ok
        days_since_last_activity = octets[1]
        threat_score = octets[2]
        type_of_visitor = octets[3]

        if type_of_visitor in BLOCKING_LEVELS.keys() or threat_score >= settings.MIN_THREAT_LEVEL:
            potential_spammer = True
        else:
            potential_spammer = False

        return (BLOCKING_LEVELS.get(type_of_visitor), potential_spammer)
    return (None, None)  # something went wrong


def send_inactive_user_mail(user):
    c = Context({'user': user})
    template_name = 'mails/new_inactive_user'

    t = loader.get_template(template_name + '.txt')
    text_content = t.render(c)
    t = loader.get_template(template_name + '.html')
    html_content = t.render(c)

    msg = EmailMultiAlternatives('Nieuwe inactieve gebruiker', text_content)
    msg.to = [admin[1] for admin in settings.ADMINS]  # email addresses
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return
