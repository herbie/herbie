from faker import Faker

from herbie_core.constants import JsonSchemaPropertiesConstants


class SchemaNumberGenerator:
    MIN_INTEGER = -9999
    MAX_INTEGER = 9999

    def __init__(self):
        self._faker = Faker()

    def generate_number(self, schema: dict) -> int:
        multiple_of = schema.get(JsonSchemaPropertiesConstants.NUMBER_TYPE_MULTIPLE_OF, None)
        minimum = schema.get(JsonSchemaPropertiesConstants.NUMBER_TYPE_MINIMUM, self.MIN_INTEGER)
        maximum = schema.get(JsonSchemaPropertiesConstants.NUMBER_TYPE_MAXIMUM, self.MAX_INTEGER)
        exclusive_maximum = schema.get(JsonSchemaPropertiesConstants.NUMBER_TYPE_EXCLUSIVE_MAXIMUM, self.MAX_INTEGER)
        exclusive_minimum = schema.get(JsonSchemaPropertiesConstants.NUMBER_TYPE_EXCLUSIVE_MINIMUM, self.MIN_INTEGER)

        maximum = min(maximum, exclusive_maximum)
        minimum = max(minimum, exclusive_minimum)

        if maximum == exclusive_maximum:
            maximum = exclusive_maximum - 1

        if minimum == exclusive_minimum:
            minimum = minimum + 1

        if multiple_of:
            numbers_allowed = [value for value in range(minimum, maximum + 1) if value % multiple_of == 0]

            return self._faker.random_elements(elements=numbers_allowed, length=1)[0]

        return self._faker.pyint(min_value=minimum, max_value=maximum)
