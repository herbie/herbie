from faker import Faker
from typing import Optional
from herbie_core.constants import JsonSchemaPropertiesConstants
from herbie_core.services.schema_mock_data.schema_data_type_mapper import SchemaDataTypeMapper


class SchemaArrayGenerator:
    def __init__(self):
        self._faker = Faker()
        self._data_type_mapper = SchemaDataTypeMapper()

    def generate_array(self, schema: dict) -> list:
        items = schema.get(JsonSchemaPropertiesConstants.ARRAY_TYPE_ITEMS, [])
        min_items = schema.get(JsonSchemaPropertiesConstants.ARRAY_TYPE_MIN_ITEMS, None)
        max_items = schema.get(JsonSchemaPropertiesConstants.ARRAY_TYPE_MAX_ITEMS, None)
        return_list = []

        if max_items == 0:
            return []

        dict_const = None

        if isinstance(items, dict):
            dict_const = self._get_const_property(items=items)
            self._process_when_dict(items=items, return_list=return_list)

        if isinstance(items, list):
            self._process_when_list(items=items, max_items=max_items, return_list=return_list)

        return self._set_proper_array_length(min_items=min_items, return_list=return_list, dict_const=dict_const)

    def _process_when_dict(self, items: dict, return_list: list) -> list:
        const = self._get_const_property(items=items)
        if const is not None:
            return_list.append(const)
        else:
            type = items[JsonSchemaPropertiesConstants.PROPERTY_TYPE]
            return_list.append(self._data_type_mapper.generate_from_data_type(type, items))

        return return_list

    def _process_when_list(self, items: list, max_items: Optional[int], return_list: list) -> list:
        if max_items is None:
            max_items = len(items)

        for item in items[:max_items]:
            const = item.get(JsonSchemaPropertiesConstants.CONST_TYPE_PROPERTY, None)
            if const is not None:
                return_list.append(self._data_type_mapper.generate_from_data_type("const", item))
                continue

            type = item[JsonSchemaPropertiesConstants.PROPERTY_TYPE]

            return_list.append(self._data_type_mapper.generate_from_data_type(type, item))

        return return_list

    def _set_proper_array_length(self, min_items: Optional[int], return_list: list, dict_const):
        if min_items is not None and len(return_list) < min_items:
            if dict_const is not None:
                return_list = return_list + [dict_const] * (min_items - len(return_list))

                return return_list

            random_list = self._faker.pylist(
                nb_elements=(min_items - len(return_list)), variable_nb_elements=False, value_types=str
            )

            return_list = return_list + random_list

        return return_list

    def _get_const_property(self, items: dict):
        return items.get(JsonSchemaPropertiesConstants.CONST_TYPE_PROPERTY, None)
