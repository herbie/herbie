from django.test import TestCase

from herbie_core.services.utils import BusinessEntityUtils


class BusinessEntityUtilsTestCase(TestCase):
    def test_snake_to_camel(self):
        self.assertEqual("", BusinessEntityUtils.snake_to_camel(""))
        self.assertEqual("Customer", BusinessEntityUtils.snake_to_camel("customer"))
        self.assertEqual("Customer", BusinessEntityUtils.snake_to_camel("customer_"))
        self.assertEqual("CustomerAddress", BusinessEntityUtils.snake_to_camel("customer_address"))

    def test_camel_to_snake(self):
        self.assertEqual("", BusinessEntityUtils.camel_to_snake(""))
        self.assertEqual("customer", BusinessEntityUtils.camel_to_snake("Customer"))
        self.assertEqual("customer_url", BusinessEntityUtils.camel_to_snake("CustomerURL"))
        self.assertEqual("customer_address", BusinessEntityUtils.camel_to_snake("CustomerAddress"))
