from django.db import models
from django.contrib.postgres.fields import JSONField
from model_utils.models import TimeStampedModel


class AbstractBusinessEntity(TimeStampedModel):
    """
    Abstract class that defines the generic data model for every business entity.
    """
    key = models.TextField(null=False)
    version = models.IntegerField(null=False, default=1)
    data = JSONField(null=False)

    class Meta:
        abstract = True
        unique_together = ('key', 'version')
