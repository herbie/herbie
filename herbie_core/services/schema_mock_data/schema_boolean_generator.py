from faker import Faker


class SchemaBooleanGenerator:
    def __init__(self):
        self._faker = Faker()

    def generate_boolean(self, schema):
        return self._faker.pybool()
