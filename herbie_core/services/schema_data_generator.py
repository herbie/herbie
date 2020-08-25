import pkgutil

from django.conf import settings


class SchemaDataGenerator:
    def __init__(self):
        a = '2'

    def mock_data_from_schema(self):
        schema = self._load()

    def _load(self) -> str:
        file_content = pkgutil.get_data(
            settings.SCHEMA_REGISTRY_PACKAGE, "customer/customer_v1.json"
        )

        return file_content.decode("utf-8")
