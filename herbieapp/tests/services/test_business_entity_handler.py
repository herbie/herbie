import unittest.mock as mock
from unittest.mock import call

from django.contrib.auth.models import User
from django.test import TestCase

from herbieapp.models import AbstractBusinessEntity
from herbieapp.services import BusinessEntityHandler, BusinessEntityUtils, MessagePublisher, BusinessEntityManager, \
    BusinessEntityCompositor, JsonSchemaValidator


class HandlerTestEntity(AbstractBusinessEntity):
    class Meta:
        managed = False


class HandlerTestCompositeEntity(AbstractBusinessEntity):
    class Meta:
        managed = False


entity_name = 'handler_test_entity'
key = '123'
version = 'v1'
test_user = User(username="test-user")
data = '{"field": "value"}'
entity = HandlerTestEntity(key=key, version=version, publisher=test_user, data=data)
composite_entity = HandlerTestCompositeEntity(key=key, version=version, publisher=test_user, data=data)


class BusinessEntityManagerTestCase(TestCase):

    def setUp(self):
        self._entity_handler = BusinessEntityHandler()

    @mock.patch.object(BusinessEntityCompositor, 'on_entity_saved', return_value=[])
    @mock.patch.object(MessagePublisher, 'send_entity_update_message')
    @mock.patch.object(BusinessEntityManager, 'update_or_create', return_value=(entity, True))
    @mock.patch.object(BusinessEntityUtils, 'get_entity_class', return_value=HandlerTestEntity)
    def test_save(self, mock_entity_utils, mock_update_or_create, mock_send_entity_update_message,
                  mock_on_entity_saved):
        created = self._entity_handler.save(entity_name, key, version, test_user, data)

        self.assertTrue(created)
        mock_update_or_create.assert_called_once()
        mock_send_entity_update_message.assert_called_once_with(entity)
        mock_on_entity_saved.assert_called_once()

    @mock.patch.object(JsonSchemaValidator, 'validate_schema', return_value={})
    @mock.patch.object(BusinessEntityCompositor, 'on_entity_saved', return_value=[composite_entity])
    @mock.patch.object(MessagePublisher, 'send_entity_update_message')
    @mock.patch.object(BusinessEntityManager, 'save')
    @mock.patch.object(BusinessEntityManager, 'update_or_create', return_value=(entity, True))
    @mock.patch.object(BusinessEntityUtils, 'get_entity_class', return_value=HandlerTestEntity)
    def test_save_with_composition(self, mock_entity_utils, mock_update_or_create, mock_save,
                                   mock_send_entity_update_message, mock_on_entity_saved, mock_validate_schema):
        created = self._entity_handler.save(entity_name, key, version, test_user, data)

        self.assertTrue(created)
        mock_update_or_create.assert_called_once()

        mock_on_entity_saved.assert_called_once()
        mock_save.assert_called_once_with(composite_entity)
        mock_validate_schema.assert_called_once()
        mock_send_entity_update_message.assert_has_calls([call(entity), call(composite_entity)], any_order=True)

    @mock.patch.object(JsonSchemaValidator, 'validate_schema', return_value={"some field": "some error"})
    @mock.patch.object(BusinessEntityCompositor, 'on_entity_saved', return_value=[composite_entity])
    @mock.patch.object(MessagePublisher, 'send_entity_update_message')
    @mock.patch.object(BusinessEntityManager, 'save')
    @mock.patch.object(BusinessEntityManager, 'update_or_create', return_value=(entity, True))
    @mock.patch.object(BusinessEntityUtils, 'get_entity_class', return_value=HandlerTestEntity)
    def test_save_with_invalid_composition(self, mock_entity_utils, mock_update_or_create, mock_save,
                                           mock_send_entity_update_message, mock_on_entity_saved, mock_validate_schema):
        created = self._entity_handler.save(entity_name, key, version, test_user, data)

        self.assertTrue(created)
        mock_update_or_create.assert_called_once()

        mock_on_entity_saved.assert_called_once()
        mock_save.assert_called_once_with(composite_entity)
        mock_validate_schema.assert_called_once()
        mock_send_entity_update_message.assert_called_once_with(entity)

    @mock.patch.object(BusinessEntityCompositor, 'on_entity_deleted', return_value=[])
    @mock.patch.object(MessagePublisher, 'send_entity_delete_message')
    @mock.patch.object(BusinessEntityManager, 'delete_by_instance', return_value=1)
    @mock.patch.object(BusinessEntityUtils, 'get_entity_class', return_value=HandlerTestEntity)
    def test_delete(self, mock_entity_utils, mock_delete_by_instance,
                    mock_send_entity_delete_message, mock_on_entity_deleted):
        deleted_count = self._entity_handler.delete_by_instance(entity)

        self.assertEqual(1, deleted_count)
        mock_delete_by_instance.assert_called_once_with(entity)
        mock_send_entity_delete_message.assert_called_once_with(entity)
        mock_on_entity_deleted.assert_called_once_with(entity)

    @mock.patch.object(BusinessEntityCompositor, 'on_entity_deleted', return_value=[composite_entity])
    @mock.patch.object(MessagePublisher, 'send_entity_delete_message')
    @mock.patch.object(BusinessEntityManager, 'delete_by_instance', return_value=1)
    @mock.patch.object(BusinessEntityUtils, 'get_entity_class', return_value=HandlerTestEntity)
    def test_delete_with_composition(self, mock_entity_utils, mock_delete_by_instance,
                                     mock_send_entity_delete_message, mock_on_entity_deleted):
        deleted_count = self._entity_handler.delete_by_instance(entity)

        self.assertEqual(1, deleted_count)
        mock_delete_by_instance.assert_has_calls([call(entity), call(composite_entity)], any_order=True)
        mock_send_entity_delete_message.assert_has_calls([call(entity), call(composite_entity)], any_order=True)
        mock_on_entity_deleted.assert_called_once_with(entity)
