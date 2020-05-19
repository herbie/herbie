from herbie.services.message_publisher.abstract_publisher import AbstractPublisher


class Registry:

    _publisher_list = {}

    @staticmethod
    def add_publisher(self, publisher: AbstractPublisher):
        self._publisher_list[publisher.get_name()] = publisher
