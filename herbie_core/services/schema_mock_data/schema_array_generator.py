from faker import Faker

from herbie_core.constants import JsonSchemaPropertiesConstants
from herbie_core.services.schema_mock_data.schema_data_type_mapper import SchemaDataTypeMapper


class SchemaArrayGenerator:
    def __init__(self):
        self._faker = Faker()
        self._data_type_mapper = SchemaDataTypeMapper()

    def generate_array(self, schema):
        items = schema.get(JsonSchemaPropertiesConstants.ARRAY_TYPE_ITEMS, [])
        min_items = schema.get(JsonSchemaPropertiesConstants.ARRAY_TYPE_MIN_ITEMS, None)
        max_items = schema.get(JsonSchemaPropertiesConstants.ARRAY_TYPE_MAX_ITEMS, None)
        return_list = []

        if max_items == 0:
            return []

        dict_const = None

        if isinstance(items, dict):
            const = items.get(JsonSchemaPropertiesConstants.CONST_TYPE_PROPERTY, None)
            if const is not None:
                dict_const = const
                return_list.append(const)
            else:
                type = items[JsonSchemaPropertiesConstants.PROPERTY_TYPE]
                return_list.append(self._data_type_mapper.generate_from_data_type(type, items))

        if isinstance(items, list):
            if max_items is None:
                max_items = len(items)

            for item in items[:max_items]:
                const = item.get(JsonSchemaPropertiesConstants.CONST_TYPE_PROPERTY, None)
                if const is not None:
                    return_list.append(self._data_type_mapper.generate_from_data_type("const", item))
                    continue

                type = item[JsonSchemaPropertiesConstants.PROPERTY_TYPE]

                return_list.append(self._data_type_mapper.generate_from_data_type(type, item))

        if min_items is not None and len(return_list) < min_items:
            if dict_const is not None:
                return_list = return_list + [dict_const] * (min_items - len(return_list))

                return return_list

            random_list = self._faker.pylist(
                nb_elements=(min_items - len(return_list)), variable_nb_elements=False, value_types=str
            )

            return_list = return_list + random_list

        return return_list
