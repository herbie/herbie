from django.core.management.base import BaseCommand

from wayneapp.services import SchemaLoader, BusinessEntityUtils

model_filename = "wayneapp/models/generated_models.py"


class Command(BaseCommand):
    help = 'Generates model classes based on the JSON schema definitions'

    def handle(self, *args, **kwargs):
        entity_names = SchemaLoader().get_all_business_entity_names()
        entity_names_camel_case = set(map(BusinessEntityUtils.snake_to_camel, entity_names))
        # entity_names = ["User", "Address", "Product"]

        w = open(model_filename, "w")
        w.write('# generated file, should not be modified manually!\n')
        w.write('from wayneapp.models import AbstractBusinessEntity\n')

        for entity_name in sorted(entity_names_camel_case):
            w.write('\n\nclass {}(AbstractBusinessEntity):\n    pass\n'.format(entity_name))

        w.close()
        self.stdout.write("Generated classes: {}".format(entity_names_camel_case))
