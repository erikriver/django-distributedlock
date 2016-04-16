from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DistributedLockAppConfig(AppConfig):
    name = 'distributedlock'
    verbose_name = _("Distributed Lock")

    def ready(self):
        import distributedlock
        self.module.autodiscover()
        for item_name in distributedlock.lock.__all__:
            item = getattr(distributedlock.lock, item_name)
            setattr(distributedlock, item_name, item)

