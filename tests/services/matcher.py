from typing import Type


class Matcher:
    """ helper class that matches attributes of an object based on a dictionary"""

    def __init__(self, type_: Type, attributes: dict):
        self.type_ = type_
        self.attributes = attributes

    def __eq__(self, other_obj):
        if not self.type_ == type(other_obj):
            return False

        for attr_name, attr_value in self.attributes.items():
            if getattr(other_obj, attr_name) != attr_value:
                return False

        return True

    def __repr__(self):
        return str(self.type_.__name__) + str(self.attributes)
