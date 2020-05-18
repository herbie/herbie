from rest_framework import serializers
from rest_framework.fields import JSONField

from herbieapp.constants import MessageActionConstants as Constants


class EntityUpdateMessage:
    def __init__(self, _type, key, version, payload, created, modified, tags):
        self.tags = tags
        self.action = Constants.UPDATE
        self.type = _type
        self.key = key
        self.version = version
        self.payload = payload
        self.created = created
        self.modified = modified

    def get_serializer(self):
        return EntityUpdateMessageSerializer(self)


class EntityDeleteMessage:
    def __init__(self, _type, key, version=None):
        self.action = Constants.DELETE
        self.type = _type
        self.key = key
        self.version = version

    def get_serializer(self):
        return EntityDeleteMessageMessageSerializer(self)

class EntityUpdateMessageSerializer(serializers.Serializer):
    tags = serializers.ListField()
    action = serializers.CharField()
    type = serializers.CharField()
    key = serializers.CharField()
    version = serializers.CharField()
    payload = JSONField()
    created = serializers.CharField()
    modified = serializers.CharField()


class EntityDeleteMessageMessageSerializer(serializers.Serializer):
    action = serializers.CharField()
    type = serializers.CharField()
    key = serializers.CharField()
    version = serializers.CharField()

