import os
import wayne_json_schema
import importlib
import pkgutil
import sys
import re

from wayneapp.messages import MessageService
from wayneapp.models.models import AbstractBusinessEntity


class BusinessEntityManager:

    _message_service = MessageService()

    def get_class(self, entity_name: str):
        models_module = importlib.import_module('wayneapp.models')

        return getattr(models_module, str(entity_name).capitalize())

    def update_or_create(
            self,
            entity_name: str,
            key: str,
            version: str,
            data: str
    ) -> (AbstractBusinessEntity, bool):
        business_entity_class = self.get_class(entity_name)
        business_entity, created = business_entity_class.objects.update_or_create(
            key=key,
            version=version,
            defaults={
                'key': key,
                'version': version,
                'data': data
            }
        )

        self._message_service.send_entity_update_message(business_entity)

        return created

    def delete(self, entity_name: str, key: str, version: str) -> None:
        business_entity_class = self.get_class(entity_name)
        business_entity_class.objects.filter(key=key, version=version).delete()

        self._message_service.send_entity_delete_message(entity_name, key, version)

    def delete_by_key(self, entity_name: str, key: str) -> None:
        business_entity_class = self.get_class(entity_name)
        business_entity_class.objects.filter(key=key).delete()


class SchemaLoader:

    def load(self, type: str, version: str) -> str:
        file_content = pkgutil.get_data('wayne_json_schema', type + '/' + type + '_' + version + '.json')
        if file_content is None:
            return '{}'
        return file_content.decode('utf-8')

    def get_all_business_entity_names(self):
        schema_directory = wayne_json_schema.__path__[0]
        business_entity_names = set()
        for (dirpath, dirnames, filenames) in os.walk(schema_directory):
            for dirname in dirnames:
                if dirname != '__pycache__':
                    business_entity_names.add(dirname)
        return business_entity_names

    def get_all_versions(self, bussines_entity_name: str):
        schema_directory = wayne_json_schema.__path__[0]
        versions = set()
        for (dirpath, dirnames, filenames) in os.walk(schema_directory):
            for filename in filenames:
                if bussines_entity_name in filename:
                    version = self._get_version_from_file_name(filename)
                    versions.add(version)
        return versions

    def _get_version_from_file_name(self, filename: str):
        data = filename.split("_")
        version = data[len(data)-1][:-5]
        return version

    def get_schema_latest_version(self, type: str) -> str:
        directory_package = os.path.dirname(sys.modules['wayne_json_schema'].__file__)
        schema_files = os.listdir(directory_package + '/' + type)

        version = 0

        for file in schema_files:
            found = re.search(type + '_v(.+?).json', file)
            found_version = int(found.group(1))
            if found_version > version:
                version = found_version

        version = 'v' + str(version)

        return version
