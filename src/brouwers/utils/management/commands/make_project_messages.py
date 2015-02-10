import os

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):

    requires_model_validation = False

    def handle_noargs(self, *args, **options):
        os.chdir(settings.PROJECT_DIR)
        call_command('makemessages', all=True, extension=['py', 'txt', 'html', 'form'])

        dirs = os.listdir(os.path.join(settings.PROJECT_DIR, 'brouwers'))
        for app in dirs:
            app_path = os.path.join(settings.PROJECT_DIR, 'brouwers', app)
            locale_path = os.path.join(app_path, "locale")
            if(os.path.exists(locale_path)):
                os.chdir(app_path)
                call_command('makemessages', all=True, extension=['py', 'txt', 'html', 'form'])
