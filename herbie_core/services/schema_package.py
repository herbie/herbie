import importlib
import json
import os
import pkgutil

from django.conf import settings


class SchemaPackage:
    def __init__(self):
        self._schema_package = importlib.import_module(settings.SCHEMA_REGISTRY_PACKAGE)

    def get_all_json_schemas(self) -> set:
        schema_directory = self._schema_package.__path__[0]

        schema_files = set()
        for (dirpath, dirnames, filenames) in os.walk(schema_directory):
            for filename in filenames:
                data = filename.split("_")
                version = data[len(data) - 1][:-5]
                business_entity = filename.rpartition("_")[0]

                if business_entity == "" or "__init_" in business_entity or version == "":
                    continue

                schema_files.add(
                    json.dumps(
                        {
                            "business_entity": business_entity,
                            "version": version,
                            "data": self._load(business_entity, version),
                        }
                    )
                )

        return schema_files

    def get_all_schema_names(self):
        schema_directory = self._schema_package.__path__[0]

        schema_names = set()
        for (dirpath, dirnames, filenames) in os.walk(schema_directory):
            for dirname in dirnames:
                if dirname != "__pycache__":
                    schema_names.add(dirname)

        return schema_names

    def _load(self, business_entity: str, version: str) -> str:
        file_content = pkgutil.get_data(
            settings.SCHEMA_REGISTRY_PACKAGE, business_entity + "/" + business_entity + "_" + version + ".json"
        )
        if file_content is None:
            return "{}"

        return file_content.decode("utf-8")
