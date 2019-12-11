from django.test import TestCase
from unittest.mock import patch
from unittest.mock import MagicMock
from rest_framework import status
from rest_framework.test import APIClient

from wayneapp.services import BusinessEntityManager, settings


class TestBusinessEntityController(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestBusinessEntityController, cls).setUpClass()
        settings.SCHEMA_PACKAGE_NAME = 'wayneapp.tests.test_schema'


    @patch.object(BusinessEntityManager, 'update_or_create', return_value={MagicMock(), True})
    def test_create_business_entity_should_work(self, mock_manager):
        data = {
            'version': 'v1',
            'key': 'x-id',
            'payload': {
                'testId': 132,
                'name': 'chris'
            }
        }

        client = APIClient()
        response = client.post('/api/test_entity/save', data, format='json')

        self.assertEqual(response.data, {'message': 'entity with key x-id created in version v1'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch.object(BusinessEntityManager, 'update_or_create', side_effect=Exception('Test'))
    def test_create_business_entity_should_fail(self, mock_manager):
        data = {
            'version': 'v1',
            'key': 'x-id',
            'payload': {
                'testId': 132,
                'name': 'chris'
            }
        }

        with self.assertRaises(Exception):
            client = APIClient()
            response = client.post('/api/test_entity/save', data, format='json')

            self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @patch.object(BusinessEntityManager, 'delete', return_value=1)
    def test_delete_business_entity_should_work(self, mock_manager):
        data = {
            'version': 'v1',
            'key': 'x-id',
        }

        client = APIClient()
        response = client.post('/api/test_entity/delete', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(BusinessEntityManager, 'delete', side_effect=Exception('Test'))
    def test_delete_business_entity_should_fail(self, mock_manager):
        data = {
            'version': 'v1',
            'key': 'x-id',
        }

        with self.assertRaises(Exception):
            client = APIClient()
            response = client.post('/api/test_entity/delete', data, format='json')

            self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
