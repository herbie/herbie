from unittest import mock
from unittest.mock import Mock

from django.test import TestCase
from herbie_core.models.models import AbstractBusinessEntity
from rest_framework import status
from rest_framework.test import APIClient


class TestUpdateBusinessEntityView(TestCase):
    def setUp(self):
        self._business_entity_mock = self._init_business_entity_mock()

    @mock.patch("herbie_core.views.update_business_entity_view.BusinessEntityManager")
    def test_update_when_no_entity_is_found(self, mock_entity_manager):
        mock_entity_manager().find_by_key_and_version.return_value = None

        client = APIClient()
        client.force_authenticate(user=None)
        response = client.patch("/entity/key/v1/update")

        self.assertIn("not found", response.data["message"])
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    @mock.patch("herbie_core.views.update_business_entity_view.BusinessEntityManager")
    @mock.patch("herbie_core.views.update_business_entity_view.JsonSchemaValidator")
    def test_update_when_schema_has_errors(self, mock_json_schema_validator, mock_entity_manager):
        mock_entity_manager().find_by_key_and_version.return_value = self._business_entity_mock
        mock_json_schema_validator().validate_schema.return_value = "Validation Error"

        client = APIClient()
        client.force_authenticate(user=None)
        response = client.patch("/entity/key/v1/update", {"test": "test"}, format="json")

        self.assertIn("Validation Error", response.data["message"])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @mock.patch("herbie_core.views.update_business_entity_view.BusinessEntityManager")
    @mock.patch("herbie_core.views.update_business_entity_view.JsonSchemaValidator")
    def test_update_returns_200(self, mock_json_schema_validator, mock_entity_manager):
        mock_entity_manager().find_by_key_and_version.return_value = self._business_entity_mock
        mock_entity_manager.update_or_create.return_value = True
        mock_json_schema_validator().validate_schema.return_value = None

        client = APIClient()
        client.force_authenticate(user=None)
        response = client.patch("/entity/key/v1/update", {"test": "test"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def _init_business_entity_mock(self):
        mock = Mock(spec=AbstractBusinessEntity)
        mock.key = "key"
        mock.version = "v1"
        mock.publisher = "publisher"
        mock.created = "2020-08-05 12:12:19"
        mock.modified = "2020-08-05 12:12:19"
        mock.data = {"name": "name"}

        return mock
