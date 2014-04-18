import time
import uuid
import logging

from django.core.cache import cache

log = logging.getLogger(__name__)


class CacheLock(object):
    """
    Try to do same as threading.Lock, but using django cache to store locks
    instance to do a distributed lock
    """

    def __init__(self, key, timeout=86400, grace=60):
        self.key = "lock:%s" % key
        self.timeout = timeout
        self.grace = grace

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
            if self.grace:
                cache.set(self.key, self.instance_id, self.grace)
            else:
                cache.delete(self.key)
        else:
            log.warn("lost lock to someone else")
