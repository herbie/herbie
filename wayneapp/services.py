import importlib
import pkgutil

from wayneapp.models.models import AbstractBusinessEntity


class BusinessEntityManager:
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

        return created

    def delete(self, entity_name: str, key: str, version: str) -> None:
        business_entity_class = self.get_class(entity_name)
        business_entity_class.objects.filter(key=key, version=version).delete()

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
