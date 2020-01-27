import unittest.mock as mock
from unittest.mock import call

from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.test import TestCase

from herbieapp.models import AbstractBusinessEntity
from herbieapp.services import BusinessEntityManager, BusinessEntityUtils, MessagePublisher


class ManagerTestEntity(AbstractBusinessEntity):
    class Meta:
        managed = False


entity_name = 'manager_test_entity'
key = '123'
version = 'v1'
test_user = User(username="test-user")
data = '{"field": "value"}'
entity = ManagerTestEntity(key=key, version=version, publisher=test_user, data=data)


class BusinessEntityManagerTestCase(TestCase):

    def setUp(self):
        self._entity_manager = BusinessEntityManager()

    @mock.patch.object(ManagerTestEntity, 'objects')
    @mock.patch.object(BusinessEntityUtils, 'get_entity_class', return_value=ManagerTestEntity)
    def test_create(self, mock_entity_utils, mock_objects):
        mock_objects.update_or_create.return_value = (entity, True)
        created_entity, created = self._entity_manager.update_or_create(entity_name, key, version, test_user, data)

        self.assertTrue(created)
        mock_objects.update_or_create.assert_called_once()

    @mock.patch.object(ManagerTestEntity, 'objects')
    @mock.patch.object(BusinessEntityUtils, 'get_entity_class', return_value=ManagerTestEntity)
    def test_update(self, mock_entity_utils, mock_objects):
        # create entity, should send one message
        mock_objects.update_or_create.return_value = (entity, False)
        created_entity, created = self._entity_manager.update_or_create(entity_name, key, version, test_user, data)

        self.assertFalse(created)
        mock_objects.update_or_create.assert_called_once()
