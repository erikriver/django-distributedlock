import uuid
import logging

from .models import Lock

log = logging.getLogger(__name__)


class DatabaseLock(object):
    """
    Try to do same as threading.Lock, but using django cache to store lock
    instance to do a distributed lock
    """

    def __init__(self, key, timeout=86400, grace=60):
        self.key = "lock:%s" % key
        self.timeout = timeout
        self.grace = grace

        # When you use threading.Lock object, instance references acts as ID of the object. In memcached
        # we have a key to identify lock, but to identify which machine/instance/thread has lock is necessary
        # put something in memcached value to identify it. So, each DatabaseLock instance has a random value to
        # identify who has the lock
        self.instance_id = uuid.uuid1().hex

    def acquire(self, blocking=True):
        lock, created = Lock.objects.get_or_create(key=self.key)
        if created:
            lock.value = self.instance_id
            lock.save()
            return True
        return False

    def release(self):
        lock = Lock.objects.get(key=self.key, value=self.instance_id)
        if lock:
            lock.delete()
        else:
            log.warn("I've no lock in DB to release. Increase TIMEOUT of lock operations")
