from uuid import uuid1

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from wayneapp import services
from wayneapp.models import User, Address


class BusinessEntityServiceTestCase(TestCase):

    def test_get_business_entity_class(self):
        user_class = services.get_business_entity_class('User')
        self.assertEquals(User, user_class)
        address_class = services.get_business_entity_class('Address')
        self.assertEquals(Address, address_class)

    def test_update_or_create_business_entity(self):
        # create user
        email = 'lars_{}@project-a.com'.format(uuid1())
        version = 1
        user_data = '{"name": "Lars"}'
        user = services.update_or_create_business_entity('User', email, version, user_data)
        self.assertIsNotNone(user)
        db_user = User.objects.get(key=email, version=version)
        self.assertEquals(user, db_user)
        self.assertEquals(email, db_user.key)
        self.assertEquals(version, db_user.version)
        self.assertEquals(user_data, db_user.data)

        # update user
        user_data = '{"name": "Herbert"}'
        user = services.update_or_create_business_entity('User', email, version, user_data)
        db_user = User.objects.get(key=email, version=version)
        self.assertEquals(user_data, db_user.data)

        # update user in new version - old version should not be changed
        version2 = 2
        user_data_v2 = '{"name": "Willi"}'
        user_v2 = services.update_or_create_business_entity('User', email, version2, user_data_v2)
        db_user_v1 = User.objects.get(key=email, version=version)
        db_user_v2 = User.objects.get(key=email, version=version2)
        self.assertEquals(user, db_user_v1)
        self.assertEquals(user_v2, db_user_v2)

    def test_delete_business_entity(self):
        email = 'lars_{}@project-a.com'.format(uuid1())
        version = 1
        user_data = '{"name": "Lars"}'
        user = services.update_or_create_business_entity('User', email, version, user_data)
        self.assertIsNotNone(User.objects.get(key=email, version=version))

        services.delete_business_entity('User', email, version)
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(key=email, version=version)
