import inject
from django.core.management.base import BaseCommand
from herbieapp.services import BusinessEntityUtils
from herbieapp.services import SchemaPackage

model_filename = "herbieapp/models/generated_models.py"


class Command(BaseCommand):
    help = 'Generates model classes based on the JSON schema definitions'
    _schema_package = None

    @inject.autoparams()
    def __init__(
            self,
            schema_package: SchemaPackage,
            **kwargs
    ):
        super().__init__(**kwargs)
        self._schema_package = schema_package

    def handle(self, *args, **kwargs):
        entity_names = self._schema_package.get_all_schema_names()
        entity_names_camel_case = set(map(BusinessEntityUtils.snake_to_camel, entity_names))

        w = open(model_filename, "w")
        w.write('# generated file, should not be modified manually!\n')
        w.write('from herbieapp.models import AbstractBusinessEntity\n')

        for entity_name in sorted(entity_names_camel_case):
            w.write('\n\nclass {}(AbstractBusinessEntity):\n    pass\n'.format(entity_name))

        w.close()
        self.stdout.write("Generated classes: {}".format(entity_names_camel_case))


