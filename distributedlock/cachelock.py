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

        # When you use threading.Lock object, instance references acts as ID of the object. In memcached
        # we have a key to identify lock, but to identify which machine/instance/thread has lock is necessary
        # put something in memcached value to identify it. So, each MemcachedLock instance has a random value to 
        # identify who has the lock
        self.instance_id = uuid.uuid1().hex

    def acquire(self, blocking=True):
        added = cache.add(self.key, self.instance_id, self.timeout)
        log.warn("Added=%s" % repr(added))
        if added:
            return True
        return False


    def release(self):
        value = cache.get(self.key)
        if value == self.instance_id:
            # Avoid short timeout, because if key expires, after GET, and another lock occurs, memcached remove
            # below can delete another lock! There is no way to solve this in memcached
            cache.delete(self.key)
        else:
            log.warn("I've no lock in Memecached to release. Increase TIMEOUT of lock operations")
