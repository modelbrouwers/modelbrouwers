from django.core.wsgi import get_wsgi_application

from brouwers.setup import setup_env

setup_env()

application = get_wsgi_application()
