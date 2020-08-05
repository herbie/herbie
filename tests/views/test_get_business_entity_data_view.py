from unittest import mock
from unittest.mock import Mock
from django.test import TestCase

from herbie_core.models.models import AbstractBusinessEntity
from rest_framework import status
from rest_framework.test import APIClient


class TestGetBusinessEntityDataView(TestCase):
    def setUp(self):
        self._business_entity_mock = self._init_business_entity_mock()

    @mock.patch("herbie_core.views.get_business_entity_data_view.BusinessEntityManager")
    def test_get_business_entity_returns_200(self, mock_entity_manager):
        mock_entity_manager().find_by_key_and_version.return_value = self._business_entity_mock

        client = APIClient()
        client.force_authenticate(user=None)
        response = client.get("/business-entity/entity/key/v1")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @mock.patch("herbie_core.views.get_business_entity_data_view.BusinessEntityManager")
    def test_get_business_when_no_entity_is_found(self, mock_entity_manager):
        mock_entity_manager().find_by_key_and_version.return_value = None

        client = APIClient()
        client.force_authenticate(user=None)
        response = client.get("/business-entity/entity/key/v1")

        self.assertIn("not found", response.data["message"])
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    @mock.patch("herbie_core.views.get_business_entity_data_view.SchemaRegistry")
    def test_get_business_with_unknown_schema(self, mock_schema_registry):
        mock_schema_registry().get_schema_latest_version.return_value = None

        client = APIClient()
        client.force_authenticate(user=None)
        response = client.get("/business-entity/entity/key")

        self.assertIn("Schema entity not found", response.data["message"])
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    @mock.patch("herbie_core.views.get_business_entity_data_view.BusinessEntityManager")
    @mock.patch("herbie_core.views.get_business_entity_data_view.SchemaRegistry")
    def test_get_business_gets_latest_version_when_none_provided(self, mock_schema_registry, mock_entity_manager):
        mock_schema_registry().get_schema_latest_version.return_value = "v2"
        mock_entity_manager().find_by_key_and_version.return_value = self._business_entity_mock

        client = APIClient()
        client.force_authenticate(user=None)
        response = client.get("/business-entity/entity/key")

        mock_entity_manager().find_by_key_and_version.assert_called_with("entity", "key", "v2")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def _init_business_entity_mock(self):
        mock = Mock(spec=AbstractBusinessEntity)
        mock.key = "key"
        mock.version = "v1"
        mock.publisher = "publisher"
        mock.created = "2020-08-05 12:12:19"
        mock.modified = "2020-08-05 12:12:19"
        mock.data = "{'name': 'name'}"

        return mock
