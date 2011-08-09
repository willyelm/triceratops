import logging
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from syncr.app.flickr import FlickrSyncr
from syncr.flickr.models import Photo, PhotoSet

logging.basicConfig(level=logging.DEBUG)

def test(blah):
    return 'success'

class Command(BaseCommand):

    help = 'Synchronize flickr feeds with Django'

    def handle(self, action='sync', **options):
        if action == 'sync':
            self.sync()
        elif action == 'reset':
            Photo.objects.all().delete()
            PhotoSet.objects.all().delete()

    def sync(self):

        f = FlickrSyncr(settings.FLICKR_API['key'],
                        settings.FLICKR_API['secret']
                        )

        for sync in settings.FLICKR_FOLLOW:
            f.syncAllPhotoSets(sync)
            logging.info('Sychronized')
