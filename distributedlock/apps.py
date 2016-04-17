from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DistributedLockAppConfig(AppConfig):
    name = 'distributedlock'
    verbose_name = _("Distributed Lock")

