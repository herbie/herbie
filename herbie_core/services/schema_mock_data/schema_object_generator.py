from faker import Faker

from herbie_core.constants import JsonSchemaPropertiesConstants
from herbie_core.services.schema_mock_data.schema_data_type_mapper import SchemaDataTypeMapper


class SchemaObjectGenerator:
    def __init__(self):
        self._faker = Faker()
        self._data_type_mapper = SchemaDataTypeMapper()

    def generate_object(self, schema: dict):
        required_fields = schema.get(JsonSchemaPropertiesConstants.PROPERTY_REQUIRED, [])

        schema_object = {}

        if schema.get(JsonSchemaPropertiesConstants.PROPERTY_PROPERTIES, None) is None:
            additional_properties = schema.get(JsonSchemaPropertiesConstants.PROPERTY_ADDITIONAL_PROPERTIES, None)

            if additional_properties is None or additional_properties is True:
                return ""

        schema_keys = schema[JsonSchemaPropertiesConstants.PROPERTY_PROPERTIES].keys()
        for key in schema_keys:
            if key in required_fields:
                schema_properties = schema[JsonSchemaPropertiesConstants.PROPERTY_PROPERTIES][key]

                const = schema.get(JsonSchemaPropertiesConstants.CONST_TYPE_PROPERTY, None)
                if const is not None:
                    schema_object[key] = self._data_type_mapper.generate_from_data_type(
                        JsonSchemaPropertiesConstants.CONST_TYPE_PROPERTY, const
                    )

                    continue

                property_type = schema_properties[JsonSchemaPropertiesConstants.PROPERTY_TYPE]
                schema_object[key] = self._data_type_mapper.generate_from_data_type(property_type, schema_properties)

        return schema_object
