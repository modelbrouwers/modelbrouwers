from django.db import connection as _connection
from models import SoftwareVersion

def connection(request):
    total_time = 0.0
    for query in _connection.queries:
        total_time += float(query.get('time', 0))
    return {'connection': _connection, 'queries_time': total_time}

def version(request):
    versions = SoftwareVersion.objects.all().order_by('-id')
    if versions:
        version = versions[0]
    else:
        version = SoftwareVersion(state='v', major=1, minor=1)
    return {'software_version': version.__unicode__()}
