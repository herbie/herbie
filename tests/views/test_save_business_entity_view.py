from django.conf import settings
from django.test import TestCase
from unittest.mock import patch
from rest_framework import status
from rest_framework.test import APIClient

from herbie_core.services.business_entity_manager import BusinessEntityManager
from herbie_core.services.permission_manager import PermissionManager


class TestSaveBusinessEntityView(TestCase):
    def setUp(self):
        self.data = {"version": "v1", "key": "x-id", "payload": {"testId": 132, "name": "chris"}}
        self.client = APIClient()

    @classmethod
    def setUpClass(cls):
        super(TestSaveBusinessEntityView, cls).setUpClass()
        settings.SCHEMA_REGISTRY_PACKAGE = "tests.test_schema"

    @patch.object(BusinessEntityManager, "update_or_create", return_value=True)
    @patch.object(PermissionManager, "has_save_permission", return_value=True)
    def test_save_business_entity_should_work(self, mock_manager, mock_controller):
        self.client.force_authenticate(user=None)
        response = self.client.post("/test_entity/save", self.data, format="json")
        self.assertEqual(response.data, {"message": "entity with key x-id created in version v1"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch.object(BusinessEntityManager, "update_or_create", return_value=False)
    @patch.object(PermissionManager, "has_save_permission", return_value=True)
    def test_update_business_entity_should_work(self, mock_manager, mock_controller):
        self.client.force_authenticate(user=None)
        response = self.client.post("/test_entity/save", self.data, format="json")
        self.assertEqual(response.data, {"message": "entity with key x-id updated in version v1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(BusinessEntityManager, "update_or_create", return_value=False)
    @patch.object(PermissionManager, "has_save_permission", return_value=True)
    def test_save_business_entity_with_no_exist_version_should_fail(self, mock_manager, mock_controller):
        self.data["version"] = "v111h"
        self.client.force_authenticate(user=None)
        response = self.client.post("/test_entity/save", self.data, format="json")
        self.assertEqual(response.data, {"message": "version v111h does not exist"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch.object(BusinessEntityManager, "update_or_create", return_value=False)
    @patch.object(PermissionManager, "has_save_permission", return_value=True)
    def test_save_business_entity_with_no_exist_schema_should_fail(self, mock_manager, mock_controller):
        self.client.force_authenticate(user=None)
        response = self.client.post("/abc/save", self.data, format="json")
        self.assertEqual(response.data, {"message": "business entity abc does not exist"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch.object(BusinessEntityManager, "update_or_create", return_value=False)
    @patch.object(PermissionManager, "has_save_permission", return_value=True)
    def test_save_business_entity_with_invalid_json_should_fail(self, mock_manager, mock_controller):
        data = {"version": "v1", "key": "x-id", "payload": {"testId": "chris"}}
        self.client.force_authenticate(user=None)
        response = self.client.post("/test_entity/save", data, format="json")
        self.assertEqual(response.data["message"]["name"]["error_message"], "'name' is a required property")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch.object(BusinessEntityManager, "update_or_create", return_value=False)
    @patch.object(PermissionManager, "has_save_permission", return_value=False)
    def test_save_business_entity_unauthorized_user_should_fail(self, mock_manager, mock_controller):
        client = APIClient()
        response = client.post("/test_entity/save", self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {"message": "unauthorized"})
