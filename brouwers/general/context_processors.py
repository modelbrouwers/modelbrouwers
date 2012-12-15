from models import SoftwareVersion

def version(request):
    versions = SoftwareVersion.objects.all().order_by('-id')
    if versions:
        version = versions[0]
    else:
        version = SoftwareVersion(state='v', major=1, minor=1)
    return {'software_version': version.__unicode__()}
