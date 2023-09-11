from django.db import models


class Lock(models.Model):
    key = models.CharField(max_length=255, blank=False, unique=True)
    value = models.CharField(max_length=255, blank=False)
    timestamp = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Lock'
        verbose_name_plural = 'Locks'

    def __unicode__(self):
        return self.key
