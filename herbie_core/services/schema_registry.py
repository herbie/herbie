from herbie_core.models.schema import Schema


class SchemaRegistry:
    def find_schema(self, business_entity: str, version: str) -> str:
        schema = Schema.objects.filter(name=business_entity, version=version).first()
        if schema is None:
            return ""

        return schema.content

    def get_all_schema_names(self):
        schema_names = Schema.objects.values_list("name", flat=True).distinct()

        return schema_names

    def get_all_versions(self, schema_name: str):
        schemas = Schema.objects.filter(name=schema_name).all()

        versions = set()
        for schema in schemas:
            versions.add(schema.version)

        return versions

    def get_schema_latest_version(self, schema_name: str) -> str:
        schema = Schema.objects.filter(name=schema_name).order_by("version").first()

        if schema is None:
            return schema

        return schema.version
