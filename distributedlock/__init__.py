import logging
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from .cachelock import CacheLock
from .databaselock import DatabaseLock

log = logging.getLogger(__name__)

DISTRIBUTEDLOCK_TIMEOUT = getattr(settings, 'DISTRIBUTEDLOCK_TIMEOUT', 60)
DISTRIBUTEDLOCK_BLOCKING = getattr(settings, 'DISTRIBUTEDLOCK_BLOCKING', True)
DISTRIBUTEDLOCK_CLIENT = getattr(settings, 'DISTRIBUTEDLOCK_CLIENT', 'cache')

if DISTRIBUTEDLOCK_CLIENT == 'cache':
    DISTRIBUTEDLOCK_FACTORY = CacheLock
elif DISTRIBUTEDLOCK_CLIENT == 'database':
    DISTRIBUTEDLOCK_FACTORY = DatabaseLock
else:
    raise ImproperlyConfigured("Unsupported lock client")


class LockNotAcquiredError(Exception):
    pass


class distributedlock(object):
    def __init__(self, key=None, lock=None, blocking=None):
        self.key = key
        self.lock = lock
        if blocking is None:
            self.blocking = DISTRIBUTEDLOCK_BLOCKING
        else:
            self.blocking = blocking

        if not self.lock:
            self.lock = DISTRIBUTEDLOCK_FACTORY(self.key, timeout=DISTRIBUTEDLOCK_TIMEOUT)

    def __call__(self, f):
        """ for use with decorator """
        if not self.key:
            self.key = "%s:%s" % (f.__module__, f.__name__)

        def wrapped(*args, **kargs):
            try:
                with self:
                    return f(*args, **kargs)
            except LockNotAcquiredError:
                log.warn("couldn't acquire lock %s" % self.key)

        return wrapped

    def __enter__(self):
        """ for use with "with" block """
        if not self.key:
            raise RuntimeError("key value required")
        if self.lock.acquire(self.blocking):
            log.debug("acquired lock %s " % self.key)
        else:
            raise LockNotAcquiredError()

    def __exit__(self, type, value, traceback):
        log.debug("releasing lock %s " % self.key)
        self.lock.release()
