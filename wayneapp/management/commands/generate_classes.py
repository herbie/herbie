from django.core.management.base import BaseCommand


model_filename = "wayneapp/models/generated_models.py"


class Command(BaseCommand):
    help = 'Generates model classes based on the JSON schema definitions'

    def handle(self, *args, **kwargs):
        # TODO get entity names from json schema definitions
        entity_names = ["User", "Address", "Product"]
        entity_names.sort()

        w = open(model_filename, "w")
        w.write('# generated file, should not be modified manually!\n')
        w.write('from wayneapp.models import GenericModel\n')

        for entity_name in entity_names:
            w.write('\n\nclass {}(GenericModel):\n    pass\n'.format(entity_name))

        w.close()
        self.stdout.write("Generated classes: {}".format(entity_names))
