__version__ = '0.2.4'

from .lock import *

try:
    # django 1.7+ will use the new AppConfig api
    # It will do this after all apps are imported.
    from django.apps import AppConfig  # noqa
    default_app_config = 'distributedlock.apps.DistributedLockAppConfig'

except ImportError:
    # Previous django versions should load module level 
    # objects into present namespace
    pass

