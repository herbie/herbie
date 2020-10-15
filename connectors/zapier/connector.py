import json
import os
import http.client
import traceback

from time import sleep
from kafka import KafkaConsumer, errors
from utils import map_message_to_zapier, to_zapier_object, \
    product_id_to_hook_url, save_zapier_execution

import logging
logging.basicConfig(
    level='INFO', format='[%(asctime)s] %(levelname)s %(message)s')

entity_name = 'funnel_exec'

starting = 0

while starting < 8:
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


def hand_off_to_zapier(entity_name, message):
    zapier_params = json.dumps(map_message_to_zapier(
        entity_name, message['payload'])).encode('ascii')
    host, path = product_id_to_hook_url(message)
    absolute_hook_path = '/' + path
    connection = http.client.HTTPSConnection(host, 443)
    connection.request('POST', absolute_hook_path, zapier_params, {
                       'Content-Type': 'application/json'})

    response_as_dict = json.loads(connection.getresponse().read())
    herbie_params = json.dumps(
        to_zapier_object(
            message['payload']['carl_id'],
            absolute_hook_path,
            response_as_dict
        )
    )
    save_zapier_execution(herbie_params)


logging.info(f'start reading messages from topic: {entity_name}')
# The iterator will be blocked forever, because we didn't set a consumer_timeout_ms parameter
# in the KafkaConsumer. So we should continuously receive any new messages.
for consumer_record in consumer:
    message = consumer_record.value
    key = message['key']
    action = message['action']
    not_processing_ratingv2 = 'zapier connector is not processing ratingv2 without completed_at set; '\
                              f'for {entity_name} messages'
    has_attribution_ratingv2 = 'zapier connector is not processing ratingv2 attribution set; '\
                               f'for {entity_name} messages'
    try:
        if action == 'create':
            if message['payload']['product_id'].lower() != 'ratingv2':
                hand_off_to_zapier(entity_name, message)
            else:
                logging.info(not_processing_ratingv2)
        elif action == 'update':
            if 'completed_at' in message['payload'] and message['payload']['product_id'].lower(
            ) == 'ratingv2':
                if 'marketing_attribution' in message['payload']:
                    logging.info(has_attribution_ratingv2)
                else:
                    hand_off_to_zapier(entity_name, message)
            else:
                logging.info(not_processing_ratingv2)
        else:
            logging.warning(
                f'zapier connector is not processing: {action} for {entity_name} messages')
    except Exception as e:
        if 'payload' in message:
            logging.error(
                f'unable to consume {message["payload"]}; ({type(e).__name__} below))')
            logging.error(traceback.format_exc())
        else:
            logging.error(
                f'unable to process message: {message} ({type(e).__name__} below)')
            logging.error(traceback.format_exc())
