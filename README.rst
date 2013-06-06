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
    ...
    'distributedlock'
    )

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

Once installed in django project::

    django-admin.py test distributedlock

Needs ``gevent`` installed only for tests purpose.


© 2013 Scryent
License BSD
