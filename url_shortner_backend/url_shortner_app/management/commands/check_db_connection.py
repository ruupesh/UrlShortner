from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError

class Command(BaseCommand):
    help = 'Check the database connection'

    def handle(self, *args, **options):
        try:
            # Try to connect to the default database
            db_conn = connections['default']
            db_conn.ensure_connection()
            self.stdout.write(self.style.SUCCESS("Database connection successful"))
        except OperationalError as e:
            self.stderr.write(self.style.ERROR(f"Database connection failed: {e}"))
