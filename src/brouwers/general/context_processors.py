from django.conf import settings
from django.db import connection as _connection


def connection(request):
    total_time = 0.0
    for query in _connection.queries:
        total_time += float(query.get('time', 0))
    return {
        'connection': _connection,
        'queries_time': total_time,
        'HONEYPOT_URL': settings.HONEYPOT_URL
        }


def djsettings(request):
    phpbb_url = settings.PHPBB_URL
    if not phpbb_url[0] == '/':
        phpbb_url = u'/{}'.format(phpbb_url)
    if not phpbb_url[-1] == '/':
        phpbb_url += '/'
    return {
        'PHPBB_URL': phpbb_url
    }
