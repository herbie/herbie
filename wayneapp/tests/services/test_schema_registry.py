from django.test import TestCase
from unittest.mock import patch
from wayneapp.services import settings

import json
import pkgutil

from wayneapp.services import SchemaRegistry


class TestSchemaRegistry(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestSchemaRegistry, cls).setUpClass()
        settings.SCHEMA_REGISTRY_PACKAGE = 'wayneapp.tests.test_schema'
        cls._schema_loader = SchemaRegistry()
        cls._business_entity = 'test_entity'
        cls._version_1 = 'v1'
        cls._version_latest = 'v2'

    @patch.object(pkgutil, 'get_data', return_value=None)
    def test_load_empty_schema(self, mock_pkgutil):
        get_json = self._schema_loader.load('test_entity', 'v1')

        self.assertEqual('{}', get_json)

    def test_load_non_existing_schema(self):
        with self.assertRaises(FileNotFoundError):
            self._schema_loader.load(self._business_entity, 'WRONG_VERSION')

        with self.assertRaises(FileNotFoundError):
            self._schema_loader.load('WRONG_ENTITY', self._version_1)

    def test_load_json_success(self):
        get_json_schema = self._schema_loader.load(self._business_entity, self._version_1)
        test_json_schema = pkgutil.get_data(settings.SCHEMA_REGISTRY_PACKAGE, self._business_entity + '/' +
                                            self._business_entity + '_' + self._version_1 + '.json')

        self.assertEqual(test_json_schema.decode('utf-8'), get_json_schema)

    def test_get_all_versions(self):
        schema_all_versions = self._schema_loader.get_all_versions(self._business_entity)

        self.assertEqual({self._version_1, self._version_latest}, schema_all_versions)

    def test_get_schema_latest_version(self):
        schema_latest_version = self._schema_loader.get_schema_latest_version(self._business_entity)

        self.assertEqual(self._version_latest, schema_latest_version)

    def test_get_all_json_schemas(self):
        schema_list = self._schema_loader.get_all_json_schemas()
        for schema in schema_list:
            schema_data = json.loads(schema)
            self.assertEqual(self._business_entity, schema_data['business_entity'])

        self.assertEqual(2, len(schema_list))
