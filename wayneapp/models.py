from django.db import models
from django.contrib.postgres.fields import JSONField
from model_utils.models import TimeStampedModel


class GenericModel(TimeStampedModel):
    key = models.TextField(null=False)
    version = models.IntegerField(null=False, default=1)
    data = JSONField(null=False)

    class Meta:
        abstract = True
        unique_together = ('key', 'version')


# automatically generate generic classes based on json schema definitions:
# $ python manage.py generate_classes
# ########################### start generic classes ###########################


class Address(GenericModel):
    pass


class Product(GenericModel):
    pass


class User(GenericModel):
    pass


# ########################### end generic classes #############################
