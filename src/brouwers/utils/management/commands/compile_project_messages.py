import os

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    requires_model_validation = False

    def handle(self, *args, **options):
        os.chdir(settings.PROJECT_DIR)
        call_command('compilemessages')

        dirs = os.listdir(os.path.join(settings.PROJECT_DIR, 'brouwers'))
        for app in dirs:
            app_path = os.path.join(settings.PROJECT_DIR, 'brouwers', app)
            locale_path = os.path.join(app_path, "locale")
            if(os.path.exists(locale_path)):
                os.chdir(app_path)
                call_command('compilemessages')
