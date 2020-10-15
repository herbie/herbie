from base64 import b64encode
from os import getenv
from strict_rfc3339 import now_to_rfc3339_utcoffset

TRACK_HOST = 'api.segment.io'
TRACK_PATH = '/v1/track'


def map_message_to_segmentcom(message):
    return {
        'event': f'Data Object {message["product_id"]}',
        'anonymousId': message["carl_id"],
        'timestamp': now_to_rfc3339_utcoffset(),
        'properties': message
    }


def map_attribution_to_segmentcom(message):
    keys = ['marketing_attribution', 'marketing_attribution_de']
    return {
        'event': f'Attribution Set {message["product_id"]}',
        'anonymousId': message["carl_id"],
        'timestamp': now_to_rfc3339_utcoffset(),
        'properties': {k: v for k, v in message.iteritems() if k in keys}
    }


def segmentcom_auth():
    return 'Basic ' + \
        b64encode(getenv('SEGMENTCOM_API_KEY').encode('ascii')).decode('ascii')
