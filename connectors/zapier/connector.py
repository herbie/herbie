import json
import os
import sys
import http.client
import traceback

from time import sleep
from kafka import KafkaConsumer, errors
from utils import *

import logging
logging.basicConfig(level='INFO', format='[%(asctime)s] %(levelname)s %(message)s')

entity_name = 'funnel_exec'

starting = 0

while starting < 3:
    starting += 1
    try:
        consumer = KafkaConsumer(bootstrap_servers=os.environ['KAFKA_URL'],
                                 value_deserializer=lambda m: json.loads(m.decode('utf-8')))
        consumer.subscribe([entity_name])
        break
    except errors.NoBrokersAvailable:
        logging.warning(f'NoBrokersAvailable retry {starting}')
        sleep(2)
        continue

logging.info(f'start reading messages from topic: {entity_name}')
# The iterator will be blocked forever, because we didn't set a consumer_timeout_ms parameter
# in the KafkaConsumer. So we should continuously receive any new messages.
for consumer_record in consumer:
    message = consumer_record.value
    key = message['key']
    action = message['action']
    try:
        if action == 'create':
            zapier_params = json.dumps(map_message_to_zapier(entity_name, message['payload'])).encode('ascii')
            host, path = PRODUCT_ID_TO_HOOK[message['payload']['product_id']].split('/', 1)
            connection = http.client.HTTPSConnection(host, 443)
            connection.request('POST', '/' + path, zapier_params, {'Content-Type': 'application/json'})
            logging.info(f'{connection.getresponse().read().decode()}')
        else:
            logging.warning(f'zapier connector is not processing: {action} for {entity_name} messages')
    except Exception as e:
        if 'payload' in message:
            logging.error(f'unable to consume {message["payload"]}; ({type(e).__name__} below))')
            logging.error(traceback.format_exc())
        else:
            logging.error(f'unable to process message: {message} ({type(e).__name__} below)')
            loggin.error(traceback.format_exc())
