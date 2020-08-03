from unittest import mock
from unittest.mock import Mock
from django.test import TestCase

from herbie_core.models.schema import Schema
from herbie_core.services.schema_registry import SchemaRegistry


class TestSchemaRegistry(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestSchemaRegistry, cls).setUpClass()
        cls._schema_registry = SchemaRegistry()
        cls._schema_name = "test_entity"
        cls._schema_content = '["json"]'
        cls._version_1 = "v1"
        cls._version_latest = "v2"

    @mock.patch.object(Schema, "objects")
    def test_schema_not_found(self, mock_objects):
        query_set = Mock(name="filter")
        query_set.first.return_value = None
        mock_objects.filter.return_value = query_set
        schema_json = self._schema_registry.find_schema(self._schema_name, self._version_1)

        self.assertEqual("", schema_json)

    @mock.patch.object(Schema, "objects")
    def test_find_schema(self, mock_objects):
        query_set = Mock(name="filter")
        query_set.first.return_value = self._get_test_schema()
        mock_objects.filter.return_value = query_set
        schema_json = self._schema_registry.find_schema(self._schema_name, self._version_1)

        self.assertEqual(self._schema_content, schema_json)

    @mock.patch.object(Schema, "objects")
    def test_get_all_versions(self, mock_objects):
        mock_filter = Mock(name="filter")
        mock_filter.all.return_value = (self._get_test_schema(), self._get_test_schema(self._version_latest))
        mock_objects.filter.return_value = mock_filter
        schema_all_versions = self._schema_registry.get_all_versions(self._schema_name)

        self.assertEqual({self._version_1, self._version_latest}, schema_all_versions)

    @mock.patch.object(Schema, "objects")
    def test_get_schema_latest_version(self, mock_objects):
        mock_filter = Mock(name="filter")
        mock_order_by = Mock(name="all")
        mock_order_by.first.return_value = self._get_test_schema(self._version_latest)
        mock_filter.order_by.return_value = mock_order_by
        mock_objects.filter.return_value = mock_filter

        schema_latest_version = self._schema_registry.get_schema_latest_version(self._schema_name)

        self.assertEqual(self._version_latest, schema_latest_version)

    def _get_test_schema(self, version=None):
        if version is None:
            version = self._version_1

        return Schema(name=self._schema_name, version=version, content=self._schema_content)
