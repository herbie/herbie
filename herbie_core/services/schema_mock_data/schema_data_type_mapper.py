from herbie_core.constants import JsonSchemaPropertiesConstants


class SchemaDataTypeMapper:
    def generate_from_data_type(self, data_type: str, schema: dict):
        from herbie_core.services.schema_mock_data.schema_array_generator import SchemaArrayGenerator
        from herbie_core.services.schema_mock_data.schema_boolean_generator import SchemaBooleanGenerator
        from herbie_core.services.schema_mock_data.schema_const_generator import SchemaConstGenerator
        from herbie_core.services.schema_mock_data.schema_number_generator import SchemaNumberGenerator
        from herbie_core.services.schema_mock_data.schema_object_generator import SchemaObjectGenerator
        from herbie_core.services.schema_mock_data.schema_string_generator import SchemaStringGenerator

        mapper = {
            JsonSchemaPropertiesConstants.DATA_TYPE_OBJECT: SchemaObjectGenerator().generate_object,
            JsonSchemaPropertiesConstants.DATA_TYPE_INTEGER: SchemaNumberGenerator().generate_number,
            JsonSchemaPropertiesConstants.DATA_TYPE_NUMBER: SchemaNumberGenerator().generate_number,
            JsonSchemaPropertiesConstants.DATA_TYPE_STRING: SchemaStringGenerator().generate_string,
            JsonSchemaPropertiesConstants.DATA_TYPE_BOOLEAN: SchemaBooleanGenerator().generate_boolean,
            JsonSchemaPropertiesConstants.DATA_TYPE_ARRAY: SchemaArrayGenerator().generate_array,
            JsonSchemaPropertiesConstants.DATA_TYPE_CONST: SchemaConstGenerator().generate_const,
        }

        return mapper[data_type](schema)
