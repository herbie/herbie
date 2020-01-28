from rest_framework import serializers
from rest_framework.fields import JSONField


class EntityUpdateMessage:
    def __init__(self, _type, key, version, payload, created, modified, tags):
        self.tags = tags
        self.action = 'update'
        self.type = _type
        self.key = key
        self.version = version
        self.payload = payload
        self.created = created
        self.modified = modified


class EntityDeleteMessage:
    def __init__(self, _type, key, version=None):
        self.action = 'delete'
        self.type = _type
        self.key = key
        self.version = version


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

