import logging
from google.api_core.exceptions import AlreadyExists
from google.cloud.pubsub_v1 import PublisherClient, SubscriberClient
from herbie import settings
from rest_framework.renderers import JSONRenderer

from herbieapp.models.message_models_serializers import EntityUpdateMessage, EntityUpdateMessageSerializer, \
    EntityDeleteMessage, EntityDeleteMessageMessageSerializer


class GooglePubSubPublisher:

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._logger = logging.getLogger(__name__)
        self._publisher = PublisherClient()
        self._subscriber = SubscriberClient()

    def send_message(self, message):
        serializer = self._get_serializer(message)

        json_data = JSONRenderer().render(serializer.data)

        topic_path = self._publisher.topic_path(settings.GCLOUD_PUBSUB_PROJECT_ID, 'customer')
        future = self._publisher.publish(topic_path, data=json_data)
        future.add_done_callback(self._publish_callback)

    def _publish_callback(self, message_future):
        if message_future.exception(timeout=30):
            self._logger.info(f'Publishing message on {message_future.exception()} threw an Exception.')
        else:
            self._logger.info(message_future.result())

    def create_topic(self, topic: str):
        topic_path = self._publisher.topic_path(settings.GCLOUD_PUBSUB_PROJECT_ID, topic)

        try:
            self._publisher.create_topic(topic_path)
        except AlreadyExists as e:
            self._logger.info(f'Topic {topic} already exists.')

    def create_subscription(self, topic: str, subscription: str):
        topic_path = self._subscriber.topic_path(settings.GCLOUD_PUBSUB_PROJECT_ID, topic)
        subscription_path = self._subscriber.subscription_path(settings.GCLOUD_PUBSUB_PROJECT_ID, subscription)

        try:
            self._subscriber.create_subscription(subscription_path, topic_path)
        except AlreadyExists as e:
            self._logger.info(f'Subscription {subscription} already exists.')
            pass

    def _get_serializer(self, message):
        if isinstance(message, EntityUpdateMessage):
            return EntityUpdateMessageSerializer(message)
        if isinstance(message, EntityDeleteMessage):
            return EntityDeleteMessageMessageSerializer(message)
        raise Exception('message model does not exist')
