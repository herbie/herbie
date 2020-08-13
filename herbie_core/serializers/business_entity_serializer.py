from rest_framework import serializers


class BusinessEntitySerializer(serializers.Serializer):
    key = serializers.CharField()
    version = serializers.CharField()
    data = serializers.CharField()
    publisher = serializers.CharField(source="publisher.username", read_only=True)
    created = serializers.CharField()
    modified = serializers.CharField()
