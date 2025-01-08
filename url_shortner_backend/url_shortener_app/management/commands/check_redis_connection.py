from django.core.management.base import BaseCommand
from django_redis import get_redis_connection
from redis.exceptions import ConnectionError

class Command(BaseCommand):
    help = 'Check the Redis connection'

    def handle(self, *args, **options):
        try:
            # Try to get a connection to Redis
            redis_conn = get_redis_connection("default")
            # Perform a ping to check if Redis is alive
            redis_conn.ping()
            self.stdout.write(self.style.SUCCESS("Redis connection successful"))
        except ConnectionError as e:
            self.stderr.write(self.style.ERROR(f"Redis connection failed: {e}"))
