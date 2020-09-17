from faker import Faker
import rstr

from herbie_core.constants import JsonSchemaPropertiesConstants


class SchemaStringGenerator:
    def __init__(self):
        self._faker = Faker()

    def generate_string(self, schema: dict) -> str:
        format = schema.get(JsonSchemaPropertiesConstants.STRING_TYPE_FORMAT, None)
        min_length = schema.get(JsonSchemaPropertiesConstants.STRING_TYPE_MIN_LENGTH, None)
        max_length = schema.get(JsonSchemaPropertiesConstants.STRING_TYPE_MAX_LENGTH, None)
        enum = schema.get(JsonSchemaPropertiesConstants.STRING_TYPE_ENUM, None)
        pattern = schema.get(JsonSchemaPropertiesConstants.STRING_TYPE_PATTERN, None)

        if pattern is not None:
            return rstr.xeger(pattern)

        if enum is not None:
            return self._faker.random_elements(elements=enum, length=1)[0]

        if min_length is not None or max_length is not None:
            if max_length is None:
                max_length = 5
            return self._faker.pystr(min_length, max_length)

        if format:
            return self._generate_from_string_format(format)

        return self._faker.name()

    def _generate_from_string_format(self, format):
        return {
            "date-time": self._faker.date_time().strftime("%Y-%m-%dT%H:%M:%S%z"),
            "date": self._faker.date_time().strftime("%Y-%m-%d"),
            "time": self._faker.date_time().strftime("%H:%M:%S"),
            "email": self._faker.ascii_email(),
            "ipv4": self._faker.ipv4(),
            "ipv6": self._faker.ipv6(),
        }[format]
