django-distributedlock
======================

A django app for functions or tasks that needs distributed lock, e.g. for management commands that used in cron jobs

Instalation
============

Install with ``pip`` in your environment::

    $ pip install django-distributedlock

Add in your ``settings.py`` in ``INSTALLED_APPS`` ::
    
    INSTALLED_APPS = (
    ...
    'distributedlock',
    ...
    )

django-distributedlock can be work with django cache or a database model, you must to set the client in the variable ``DISTRIBUTEDLOCK_CLIENT``, with the values ``cache`` or ``database`` according your needs.::

    DISTRIBUTEDLOCK_CLIENT="cache"       # or "database"


Use
===

For register a distrbuted function with decorator::

   from distributedlock import distributedlock

   @distributedlock()
   def my_task():
       print "running"

or you can use the sentence ``with``::

    with distributedlock('my_key_task'):
        print 'running'

Tests
=====

Once installed in your django project::

    django-admin.py test distributedlock

Needs ``gevent`` installed only for tests purpose.

Some ideas were take from https://github.com/snbuback/DistributedLock

© 2013 Scryent
License BSD
