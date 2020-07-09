import sys

from google.api_core.exceptions import AlreadyExists
from google.cloud.pubsub_v1 import SubscriberClient


class PubSubConsumer:
    GCLOUD_PUBSUB_PROJECT_ID = 'herbie-app'

    def __init__(self):
        self._subscriber = SubscriberClient()

    def create_subscription(self, topic: str, subscription: str):
        topic_path = self._subscriber.topic_path(self.GCLOUD_PUBSUB_PROJECT_ID, topic)
        subscription_path = self._subscriber.subscription_path(self.GCLOUD_PUBSUB_PROJECT_ID, subscription)

        try:
            self._subscriber.create_subscription(subscription_path, topic_path)
        except AlreadyExists as e:
            print(f'Subscription {subscription} already exists.')
            pass

    def subscribe(self, subscription: str):
        project_id = self.GCLOUD_PUBSUB_PROJECT_ID
        subscription_path = self._subscriber.subscription_path(project_id, subscription)

        future = self._subscriber.subscribe(subscription_path, self._subscribe_callback)

        print(f'Listening for messages on {subscription_path}')

        try:
            future.result()
        except KeyboardInterrupt:
            future.cancel()

    def _subscribe_callback(self, message):
        print(message.data)


if len(sys.argv) < 2:
    print('Please provide a Topic to subscribe to e.g: "python kafka_consumer.py test"')
    exit()

topic = sys.argv[1]

consumer = PubSubConsumer()
consumer.create_subscription(topic, 'subscription_customer')
consumer.subscribe('subscription_customer')
