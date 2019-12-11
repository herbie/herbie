from django.test import TestCase

from wayneapp.services import BusinessEntityUtils


class BusinessEntityUtilsTestCase(TestCase):

    def test_snake_to_camel(self):
        self.assertEquals('', BusinessEntityUtils.snake_to_camel(''))
        self.assertEquals('Customer', BusinessEntityUtils.snake_to_camel('customer'))
        self.assertEquals('Customer', BusinessEntityUtils.snake_to_camel('customer_'))
        self.assertEquals('CustomerAddress', BusinessEntityUtils.snake_to_camel('customer_address'))

    def test_camel_to_snake(self):
        self.assertEquals('', BusinessEntityUtils.camel_to_snake(''))
        self.assertEquals('customer', BusinessEntityUtils.camel_to_snake('Customer'))
        self.assertEquals('customer_url', BusinessEntityUtils.camel_to_snake('CustomerURL'))
        self.assertEquals('customer_address', BusinessEntityUtils.camel_to_snake('CustomerAddress'))
