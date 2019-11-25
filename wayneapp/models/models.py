from django.db import models
from django.contrib.postgres.fields import JSONField
from model_utils.models import TimeStampedModel


class GenericModel(TimeStampedModel):
    """
    Abstract class that defines the generic data model for every business object.
    Concrete implementations can be generated based on the json schema definitions
    by executing this manage command:

    $ python manage.py generate_classes
    """
    key = models.TextField(null=False)
    version = models.IntegerField(null=False, default=1)
    data = JSONField(null=False)

    class Meta:
        abstract = True
        unique_together = ('key', 'version')


class GenericModelTest(GenericModel):
    pass
