import unittest.mock as mock
from unittest.mock import call

from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.test import TestCase

from herbie_core.models.models import AbstractBusinessEntity
from herbie_core.services.business_entity_manager import BusinessEntityManager
from herbie_core.services.message_publisher.message_publisher import MessagePublisher
from herbie_core.services.utils import BusinessEntityUtils


class ManagerTestEntity(AbstractBusinessEntity):
    class Meta:
        managed = False
        app_label = "herbie_core"


entity_name = "manager_test_entity"
key = "123"
version = "v1"
test_user = User(username="test-user")
data = '{"field": "value"}'
entity = ManagerTestEntity(key=key, version=version, publisher=test_user, data=data)


class BusinessEntityManagerTestCase(TestCase):
    def setUp(self):
        self._entity_manager = BusinessEntityManager()

    @mock.patch.object(MessagePublisher, "send_entity_create_message")
    @mock.patch.object(ManagerTestEntity, "objects")
    @mock.patch.object(BusinessEntityUtils, "get_entity_class", return_value=ManagerTestEntity)
    def test_create(self, mock_entity_utils, mock_objects, mock_send_entity_create_message):
        mock_objects.update_or_create.return_value = (entity, True)
        created = self._entity_manager.update_or_create(entity_name, key, version, test_user, data)

        self.assertTrue(created)
        mock_objects.update_or_create.assert_called_once()
        mock_send_entity_create_message.assert_called_once_with(entity)

    @mock.patch.object(MessagePublisher, "send_entity_update_message")
    @mock.patch.object(ManagerTestEntity, "objects")
    @mock.patch.object(BusinessEntityUtils, "get_entity_class", return_value=ManagerTestEntity)
    def test_update(self, mock_entity_utils, mock_objects, mock_send_entity_update_message):
        mock_objects.update_or_create.return_value = (entity, False)
        created = self._entity_manager.update_or_create(entity_name, key, version, test_user, data)

        self.assertFalse(created)
        mock_objects.update_or_create.assert_called_once()
        mock_send_entity_update_message.assert_called_once_with(entity)

    @mock.patch.object(MessagePublisher, "send_entity_delete_message")
    @mock.patch.object(QuerySet, "delete")
    @mock.patch.object(QuerySet, "all")
    @mock.patch.object(BusinessEntityUtils, "get_entity_class", return_value=ManagerTestEntity)
    def test_delete(self, mock_entity_utils, mock_queryset_all, mock_queryset_delete, mock_send_entity_delete_message):
        mock_queryset_all.return_value = [entity]
        mock_queryset_delete.return_value = (1, {})
        delete_count = self._entity_manager.delete(entity_name, key, version)

        self.assertEqual(1, delete_count)
        mock_send_entity_delete_message.assert_called_once_with(entity)

    @mock.patch.object(MessagePublisher, "send_entity_delete_message")
    @mock.patch.object(QuerySet, "delete")
    @mock.patch.object(QuerySet, "all")
    @mock.patch.object(BusinessEntityUtils, "get_entity_class", return_value=ManagerTestEntity)
    def test_delete_by_key(
        self, mock_entity_utils, mock_queryset_all, mock_queryset_delete, mock_send_entity_delete_message
    ):
        mock_queryset_all.return_value = [entity, entity]
        mock_queryset_delete.return_value = (2, {})
        delete_count = self._entity_manager.delete_by_key(entity_name, key)

        self.assertEqual(2, delete_count)
        mock_send_entity_delete_message.assert_has_calls([call(entity), call(entity)])

    @mock.patch.object(ManagerTestEntity, "objects")
    @mock.patch.object(BusinessEntityUtils, "get_entity_class", return_value=ManagerTestEntity)
    def test_find_by_key_and_version(self, mock_entity_utils, mock_objects):
        mock_objects.get.return_value = entity

        entity_data = self._entity_manager.find_by_key_and_version(entity_name, key, version)

        self.assertEqual(entity_data, entity)

    @mock.patch.object(ManagerTestEntity, "objects")
    @mock.patch.object(BusinessEntityUtils, "get_entity_class", return_value=ManagerTestEntity)
    def test_find_by_key_and_version_returns_none_when_not_found(self, mock_entity_utils, mock_objects):
        mock_objects.get.side_effect = ManagerTestEntity.DoesNotExist

        self.assertIsNone(self._entity_manager.find_by_key_and_version(entity_name, "random", version))
