import unittest.mock as mock
from unittest.mock import call

from django.contrib.auth.models import User
from django.test import TestCase

from herbieapp.models import AbstractBusinessEntity, Schema
from herbieapp.services import BusinessEntityHandler, BusinessEntityUtils, MessagePublisher, BusinessEntityManager, \
    BusinessEntityCompositor, JsonSchemaValidator


class PriceTestEntity(AbstractBusinessEntity):
    class Meta:
        managed = False


class ProductDescriptionTestEntity(AbstractBusinessEntity):
    class Meta:
        managed = False


class ProductTestEntity(AbstractBusinessEntity):
    class Meta:
        managed = False


version = 'v1'
join_key = 'ABC-123'
test_user = User(username="test-user")
composite_entity_name = 'product_test_entity'

price_data = {"productId": join_key, "value": 0.99, "currency": "€"}
price = PriceTestEntity(key='price1', version=version, publisher=test_user, data=price_data)

description_data = {"productId": join_key, "name": "Apple", "description": "red"}
product_description = ProductDescriptionTestEntity(key='desc1', version=version, publisher=test_user,
                                                   data=description_data)

incomplete_product = ProductTestEntity(key=join_key, version=version, publisher=test_user,
                                       data=description_data.copy())

complete_product = ProductTestEntity(key=join_key, version=version, publisher=test_user,
                                     data={**description_data, **price_data})


class BusinessEntityCompositorTestCase(TestCase):

    def setUp(self):
        self._entity_compositor = BusinessEntityCompositor()

    @mock.patch.object(BusinessEntityManager, 'get_entity', return_value=None)
    @mock.patch.object(BusinessEntityUtils, 'get_entity_class', return_value=ProductTestEntity)
    def test_on_entity_saved_incomplete(self, mock_get_entity_class, mock_get_entity):
        composite_entities = self._entity_compositor.on_entity_saved(product_description, test_user)

        self.assertEqual(1, len(composite_entities))
        mock_get_entity.assert_called_once_with(composite_entity_name, join_key, version)

        # the composite_entity didn't exist before, so a new one should be created, containing only the description_data
        composite_entity = composite_entities[0]
        self.assertEqual(join_key, composite_entity.key)
        self.assertEqual(version, composite_entity.version)
        self.assertEqual(test_user, composite_entity.publisher)
        self.assertEqual(description_data, composite_entity.data)

    @mock.patch.object(BusinessEntityManager, 'get_entity', return_value=incomplete_product)
    @mock.patch.object(BusinessEntityUtils, 'get_entity_class', return_value=ProductTestEntity)
    def test_on_entity_saved_complete(self, mock_get_entity_class, mock_get_entity):
        composite_entities = self._entity_compositor.on_entity_saved(price, test_user)

        self.assertEqual(1, len(composite_entities))
        mock_get_entity.assert_called_once_with(composite_entity_name, join_key, version)

        # the composite_entity existed before, containing the description_data.
        # so now it should also contain the price data
        composite_entity = composite_entities[0]
        self.assertEqual(complete_product.key, composite_entity.key)
        self.assertEqual(complete_product.version, composite_entity.version)
        self.assertEqual(complete_product.publisher, composite_entity.publisher)
        self.assertTrue(complete_product.data == composite_entity.data)

    @mock.patch.object(BusinessEntityManager, 'get_entity', return_value=complete_product)
    @mock.patch.object(BusinessEntityUtils, 'get_entity_class', return_value=ProductTestEntity)
    def test_on_entity_deleted(self, mock_get_entity_class, mock_get_entity):
        composite_entities = self._entity_compositor.on_entity_deleted(price)

        self.assertEqual(1, len(composite_entities))
        mock_get_entity.assert_called_once_with(composite_entity_name, join_key, version)

        composite_entity = composite_entities[0]
        self.assertEqual(complete_product.key, composite_entity.key)
        self.assertEqual(complete_product.version, composite_entity.version)
