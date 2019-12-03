import os
import wayne_json_schema
import importlib
import pkgutil

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
        if file_content == None:
            json_string = '{}'
        else:
            json_string = file_content.decode('utf-8')

        return json_string

    def get_all_business_entity_names(self):
        schema_directory = wayne_json_schema.__path__[0]
        business_entity_names = set()
        for (dirpath, dirnames, filenames) in os.walk(schema_directory):
            for dirname in dirnames:
                if dirname != '__pycache__':
                    business_entity_names.add(''.join(x.capitalize() or '_' for x in dirname.split('_')))

        return business_entity_names
