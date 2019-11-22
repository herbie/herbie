from django.core.management.base import BaseCommand


model_filename = "wayneapp/models.py"
generic_block_start = "# ########################### start generic classes ###########################\n"
generic_block_end = "# ########################### end generic classes #############################\n"


class Command(BaseCommand):
    help = 'Generates model classes based on the JSON schema definitions'

    def handle(self, *args, **kwargs):
        # TODO get entity names from json schema definitions
        entity_names = ["User", "Address", "Product"]
        entity_names.sort()

        r = open(model_filename, "r")
        lines = r.readlines()
        r.close()

        w = open(model_filename, "w")
        inside_generic = False
        generic_block_found = False
        for line in lines:
            if line == generic_block_start:
                inside_generic = True
                generic_block_found = True
                w.write(line)
                for entity_name in entity_names:
                    w.write('\n\nclass {}(GenericModel):\n    pass\n'.format(entity_name))
            elif line == generic_block_end:
                inside_generic = False
                w.write('\n\n' + line)
            elif inside_generic:
                pass
            else:
                w.write(line)
        w.close()

        if generic_block_found:
            self.stdout.write("Generated classes: {}".format(entity_names))
        else:
            self.stdout.write("ERROR: now generic classes block found in models.py!")
