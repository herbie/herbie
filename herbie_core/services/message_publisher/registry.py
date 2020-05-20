from herbie_core.services.message_publisher.abstract_publisher import AbstractPublisher


class Registry:

    _publisher_list = {}

    @staticmethod
    def add_publisher(publisher: AbstractPublisher):
        Registry._publisher_list[publisher.get_name()] = publisher

    @staticmethod
    def get_publisher(name: str) -> AbstractPublisher:
        if name not in Registry._publisher_list:
            raise Exception

        return Registry._publisher_list[name]

    @staticmethod
    def get_publisher_list() -> dict:
        return Registry._publisher_list
