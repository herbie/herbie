from django.test import TestCase
from rest_framework import status
from wayneapp.models import GenericModelTest, User
from rest_framework.test import APIRequestFactory, APIClient


class ControllerPathVariablesTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(ControllerPathVariablesTest, cls).setUpClass()
        User.objects.create(key="1", version=1, data={})

    def test_ControllerPathVariables_should_work(self):
        data = {
            "object": {
                "id": 1,
                "fname": "chris"
            }
        }
        client = APIClient()
        response = client.post('/api/User/1', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

