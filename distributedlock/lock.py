import logging

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from .cachelock import CacheLock
from .databaselock import DatabaseLock

__all__ = (
    'distributedlock', 
    'LockNotAcquiredError',
    'CacheLock',
    'DatabaseLock'
)

log = logging.getLogger(__name__)


DISTRIBUTEDLOCK_TIMEOUT = getattr(settings, 'DISTRIBUTEDLOCK_TIMEOUT', 60)
DISTRIBUTEDLOCK_BLOCKING = getattr(settings, 'DISTRIBUTEDLOCK_BLOCKING', True)
DISTRIBUTEDLOCK_CLIENT = getattr(settings, 'DISTRIBUTEDLOCK_CLIENT', 'cache')


class LockNotAcquiredError(Exception):
    pass


class distributedlock(object):
    def __init__(self, key=None, lock=None, blocking=None):
        self.lock = lock
        if blocking is None:
            self.blocking = DISTRIBUTEDLOCK_BLOCKING
        else:
            self.blocking = blocking

        # for use with decorator
        if not self.lock and not key:
            key = "%s:%s" % (f.__module__, f.__name__)

        if not self.lock:
            LockFactory = self.get_lock_factory()
            self.lock = LockFactory(key, timeout=DISTRIBUTEDLOCK_TIMEOUT)

    def __call__(self, f):
        """ for use with decorator """

        def wrapped(*args, **kargs):
            try:
                with self:
                    return f(*args, **kargs)
            except LockNotAcquiredError:
                log.warning("couldn't acquire lock {}".format(self.lock.key))

        return wrapped

    def __enter__(self):
        """ for use with "with" block """
        if not self.lock.key:
            raise RuntimeError("key value required")

        if self.lock.acquire(self.blocking):
            log.debug("acquired lock {}".format(self.lock.key))
        else:
            raise LockNotAcquiredError()

    def __exit__(self, type, value, traceback):
        log.debug("releasing lock {}".format(self.lock.key))
        self.lock.release()

    def get_lock_factory(self):
        LockFactory = {
            'cache': CacheLock,
            'database': DatabaseLock,
        }.get(DISTRIBUTEDLOCK_CLIENT)

        if not LockFactory:
            msg = "Unsupported lock client: {}".format(LockFactory)
            raise ImproperlyConfigured(msg)

        return LockFactory

