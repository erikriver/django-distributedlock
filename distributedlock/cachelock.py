import time
import uuid
import logging

from django.core.cache import cache

log = logging.getLogger(__name__)


class CacheLock(object):
    """
    Try to do same as threading.Lock, but using django cache to store lock instance to do a distributed lock
    """

    def __init__(self, key, timeout=60):
        self.key = "lock:%s" % key
        self.timeout = timeout

        # uniquely identify who has the lock
        self.instance_id = uuid.uuid1().hex

    def acquire(self, blocking=True):
        added = cache.add(self.key, self.instance_id, self.timeout)
        if added:
            return True
        return False

    def release(self):
        value = cache.get(self.key)
        if value == self.instance_id:
            # Avoid short timeout, because if key expires, after GET, and
            # another lock occurs, memcached remove below can delete
            # another lock!
            # TODO: fix this by storing timeout value in cache and caching
            # forever.
            cache.delete(self.key)
        else:
            log.warn("tried to release invalid lock.  Increase TIMEOUT of lock operations")
