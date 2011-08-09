import logging
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from syncr.app.tweet import TwitterSyncr
from syncr.twitter.models import Tweet

logging.basicConfig(level=logging.DEBUG)

def test(blah):
    return 'success'

class Command(BaseCommand):

    help = 'Synchronize twitter feeds with Django'

    def handle(self, action='sync', **options):
        if action == 'sync':
            self.sync()
        elif action == 'reset':
            Tweet.objects.all().delete()

    def sync(self):

        t = TwitterSyncr(settings.TWITTER_OAUTH['username'],
                         settings.TWITTER_OAUTH['consumer_key'],
                         settings.TWITTER_OAUTH['consumer_secret'],
                         settings.TWITTER_OAUTH['token_key'],
                         settings.TWITTER_OAUTH['token_secret'],
                        )

        for sync in settings.TWITTER_FOLLOW:
            t.syncUser(sync)
            t.syncTwitterUserTweets(sync)
            logging.info('Sychronized')
