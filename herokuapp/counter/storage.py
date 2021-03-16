import redis
from django.conf import settings


class Counter:
    redis = None
    key = "counter_key"

    def __init__(self):
        if settings.REDIS_URL:
            self.redis = redis.from_url(settings.REDIS_URL)
        else:
            self.x = 0

    def inc(self):
        if settings.REDIS_URL:
            return self.redis.incr(self.key)
        else:
            self.x += 1
            return self.x


counter = Counter()
