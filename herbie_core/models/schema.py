from django.db import models
from django.contrib.postgres.fields import JSONField
from model_utils.models import TimeStampedModel


class Schema(TimeStampedModel):
    name = models.TextField(null=False)
    version = models.TextField(null=False)
    content = JSONField(null=False)
