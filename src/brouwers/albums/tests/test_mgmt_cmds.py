from django.core.management import call_command
from django.db.models import signals
from django.test import TestCase, override_settings

import factory
from sorl.thumbnail.models import KVStore

from .factories import PhotoFactory


class CommandTests(TestCase):
    """
    Test the management commands
    """

    @factory.django.mute_signals(signals.post_save)
    @override_settings(THUMBNAIL_KVSTORE="sorl.thumbnail.kvstores.dbm_kvstore.KVStore")
    def test_generate_thumbs(self):
        """
        Test that the thumbnails are generated for all photos in the management
        command `generate thumbs`.
        """
        PhotoFactory.create_batch(3)

        qs = KVStore.objects.all()
        self.assertEqual(
            qs.count(), 0
        )  # verifies that the signal is indeed properly disconnected

        call_command("generate_thumbs")

        self.assertGreaterEqual(qs.count(), 9)
