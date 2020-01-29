import json

import sys
from kafka import KafkaConsumer

if len(sys.argv) < 2:
    print('please provide an entity name parameter when running the script, e.g. "python kafka_consumer.py customer"')
    exit()

entity_name = sys.argv[1]

# Configuring the Kafka consumer to retrieve all messages that are currently stored in Kafka.
# To receive only new messages, you can remove the auto_offset_reset parameter.
consumer = KafkaConsumer(bootstrap_servers='herbie-kafka:9093',
                         auto_offset_reset='earliest',
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')))
consumer.subscribe([entity_name])

print(f'start reading messages from topic: {entity_name}')
# The iterator will be blocked forever, because we didn't set a consumer_timeout_ms parameter
# in the KafkaConsumer. So we should continuously receive any new messages.
for consumer_record in consumer:
    message = consumer_record.value
    key = message['key']
    action = message['action']
    if action == 'update':
        print(f'saving {entity_name} with id {key} to database: {message["payload"]}')
        # ...
    elif action == 'delete':
        print(f'deleting {entity_name} with id {key} from database')
        # ...
    else:
        print(f'ignoring unknown message action: {action}')
