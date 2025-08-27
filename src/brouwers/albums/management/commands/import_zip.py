import argparse
import logging
import os
from zipfile import ZipFile

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Imports the missing image files for an user"

    def add_arguments(self, parser):
        parser.add_argument("username")
        parser.add_argument("--zip", nargs="+", type=argparse.FileType("r"))

    def handle(self, **options):
        user = get_user_model().objects.get(username__iexact=options["username"])

        def get_name(photo):
            return os.path.split(photo.image.name)[-1]

        deleted = {
            get_name(photo): photo for photo in user.photo_set.all() if not photo.exists
        }

        for infile in options["zip"]:
            zipfile = ZipFile(infile)
            for name in zipfile.namelist():
                bits = os.path.splitext(name)
                bits = bits[0], bits[-1].lower()  # normalize extension
                _name = "".join(bits)
                try:
                    photo = deleted[_name]
                except KeyError:
                    self.stdout.write("Skipping %s: photo file exists" % name)
                    continue

                directory = os.path.split(photo.image.path)[0]
                if not os.path.exists(directory):
                    os.makedirs(directory)
                with open(photo.image.path, "w") as photo_file:
                    photo_file.write(zipfile.read(name))

                del deleted[_name]

        for name, photo in deleted.items():
            self.stdout.write("Still missing: %s" % photo.image.path)
        self.stdout.write("(%d images)" % len(deleted))
