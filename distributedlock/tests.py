import time
from django.test import TestCase
from django.test.utils import override_settings

from distributedlock import distributedlock
from distributedlock.cachelock import CacheLock
from distributedlock.databaselock import DatabaseLock

import logging
logging.basicConfig()

@override_settings(DISTRIBUTEDLOCK_CLIENT='cache')
class LockCacheTestCase(TestCase):

    def setUp(self):
        self.lock = CacheLock(key='periodic_task')

    def test_decorated_function(self):

        @distributedlock(lock=self.lock)
        def periodic_task():
            return True

        self.assertTrue(periodic_task())

    def test_with_function(self):

    	def bar(t):
            time.sleep(t)
            return t

        foo = 0
    	with distributedlock(key='periodic_task', lock=self.lock):
            foo = bar(1)

        self.assertEqual(foo, 1)

    def test_concurrent_tasks(self):
        import gevent

        self.foo = 0

        @distributedlock(lock=self.lock)
        def parallel_task(t):
            self.foo = t
            gevent.sleep(t)
            time.sleep(t)

        gevent.joinall([
            gevent.spawn(parallel_task, 3),
            gevent.spawn(parallel_task, 2),
            gevent.spawn(parallel_task, 1),
        ])

        self.assertEqual(self.foo, 3)

    def test_raise_exception_task(self):
        import gevent

        @distributedlock(key='error_task', lock=self.lock)
        def bar():
            raise RuntimeError
            print "error!"

        self.assertRaises(RuntimeError, bar)


@override_settings(DISTRIBUTEDLOCK_CLIENT='database')
class LockDatabaseTestCase(LockCacheTestCase):

    def setUp(self):
        self.lock = DatabaseLock(key='periodic_task2')
