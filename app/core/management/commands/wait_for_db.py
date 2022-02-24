from email.policy import default
import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """Djanco command to pause exec until db is avaliable"""

    def handle(self, *args, **options):
        self.stdout.write('Waiting for Database...')
        db_conn = None

        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Databas Unavailable, wating one second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))