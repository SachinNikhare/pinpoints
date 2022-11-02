from django.core.management.base import BaseCommand, CommandError
from shortener.models import pinpointsURL

class Command(BaseCommand):
    help = 'Refreshes all pinpointsURL shortcode'

    def add_arguments(self, parser):
        parser.add_argument('items', type=int)

    def handle(self, *args, **options):
        return pinpointsURL.objects.refresh_shortcode(items=options['items'])