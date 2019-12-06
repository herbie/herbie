import os
import pkgutil
import re
from django.conf import settings
import importlib


class SchemaLoader:
    def __init__(self):
        self._schema_package = importlib.import_module(settings.SCHEMA_PACKAGE_NAME)

    def load(self, business_entity: str, version: str) -> str:
        file_content = pkgutil.get_data(settings.SCHEMA_PACKAGE_NAME, business_entity + '/' + business_entity + '_' + version + '.json')
        if file_content is None:
            return '{}'

        return file_content.decode('utf-8')

    def get_all_business_entity_names(self):
        schema_directory = self._schema_package.__path__[0]
        business_entity_names = set()
        for (dirpath, dirnames, filenames) in os.walk(schema_directory):
            for dirname in dirnames:
                if dirname != '__pycache__':
                    business_entity_names.add(dirname)

        return business_entity_names

    def get_all_versions(self, bussiness_entity_name: str):
        schema_directory = self._schema_package.__path__[0]
        versions = set()
        for (dirpath, dirnames, filenames) in os.walk(schema_directory):
            for filename in filenames:
                if bussiness_entity_name in filename:
                    version = self._get_version_from_file_name(filename)
                    versions.add(version)

        return versions

    def _get_version_from_file_name(self, filename: str):
        data = filename.split("_")
        version = data[len(data)-1][:-5]

        return version

    def get_schema_latest_version(self, business_entity: str) -> str:
        directory_package = os.path.dirname(self._schema_package.__file__)
        schema_files = os.listdir(directory_package + '/' + business_entity)

        version = 0

        for file in schema_files:
            found = re.search(business_entity + '_v(.+?).json', file)
            found_version = int(found.group(1))
            if found_version > version:
                version = found_version

        version = 'v' + str(version)

        return version
