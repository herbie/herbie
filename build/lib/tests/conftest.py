import os, fnmatch

import pytest

from django.core.management import call_command


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
   with django_db_blocker.unblock():
       test_path = os.path.dirname(os.path.realpath(__file__))

       fixtures = fnmatch.filter(os.listdir(test_path + '/fixtures'), '*.json')

       for fixture in fixtures:
           call_command('loaddata', test_path + '/fixtures/' + fixture)
