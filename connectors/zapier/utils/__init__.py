import http.client
import logging

from datetime import datetime
from uuid import uuid4
from os import environ

STORE_KEY = environ['HERBIE_TOKEN']
STORE_HOST = environ['HERBIE_HOST']
STORE_PATH = '/api/zapier_start/save'

MAPPING = {
    '_ga': 'ga_session_id',
    '_gid': 'ga_user_id',
    'adgroupid': 'ga_adgroup_id',
    'age': 'person_age',
    'ageTax': 'is_person_age_55',
    'ageTax_de': 'is_person_age_55_de',
    'appFunnel': '',  # what to map from?
    'carlId': 'carl_id',
    'corporateForm': 'company_corporate_form',
    'dateActivity': 'lead_set_activity_at',
    'degree': 'person_degree',
    'degree_de': 'person_degree_de',
    'dependencyOwner': 'company_dependency_owner',
    'dependencyOwner_de': 'company_dependency_owner_de',
    'device': 'ga_device',
    'digitalizationChallenge1': 'digitalization_challenge_question_1',
    'digitalizationChallenge1_de': 'digitalization_challenge_question_1_de',
    'dynamickey': 'ga_dynamickey',
    'ebitMultiple': 'company_ebit_multiple',
    'email': 'person_email',
    'employees': 'company_count_employees_range',
    'evavg': 'company_enterprise_value_avg',
    'evavg-Carl': '',  # what to map from
    'evavgNoCarlRounded': 'company_enterprise_value_avg_80_rounded',
    'evavgRounded': 'company_enterprise_value_avg_rounded',
    'evmax': 'company_enterprise_value_max',
    'evmax-Carl': '',  # what to map from
    'evmaxNoCarlRounded': 'company_enterprise_value_max_80_rounded',
    'evmaxRounded': 'company_enterprise_value_max_rounded',
    'evmin': 'company_enterprise_value_min',
    'evmin-Carl': '',  # what to map from
    'evminNoCarlRounded': 'company_enterprise_value_min_80_rounded',
    'evminRounded': 'company_enterprise_value_min_rounded',
    'familyBusiness': 'is_company_family_business',
    'familyBusiness_de': 'is_company_family_business_de',
    'financingChallenge': 'digitalization_challenge_question_2',
    'financingChallenge_de': 'digitalization_challenge_question_2_de',
    'firstname': 'person_first_name',
    'focus': 'person_focus',
    'focus_de': 'person_focus_de',
    'foundingDate': 'company_founding_time_range',
    'funnelID': '',  # what to map from
    'gclid': 'ga_gclid',
    'gender': 'person_gender',
    'keyword': 'ga_keyword',
    'largestCustomer': 'company_share_largest_customer',
    'lastname': 'person_last_name',
    'matchtype': 'ga_matchtype',
    'name': 'person_name',
    'network': 'ga_network',
    'numberCustomer': 'company_number_customer_range',
    'pageID': 'page_id',
    'phone': 'person_phone',
    'productID': 'product_id',
    'profit': 'company_ebit',
    'revenue': 'company_revenue',
    'revenueMultiple': 'company_revenue_multiple',
    'saleDate': 'company_sale_date',
    'saleDate_de': 'company_sale_date_de',
    'salePrice': 'company_sale_price',
    'sector': 'company_industry',
    'sector_de': 'company_industry_de',
    'shareholderType': 'is_person_type',
    'shareholderType_de': 'is_person_type_de',
    'successionAim': 'company_sale_reason',
    'successionAim_de': 'company_sale_reason_de',
    'successorType': 'company_sale_target',
    'successorType_de': 'company_sale_target_de',
    'timeHolding': 'company_duration_stake_holding',
    'timeHolding_de': 'company_duration_stake_holding',
    'timestamp': 'lead_created_at',
    'utm_campaignid': 'utm_campaign_id',
    'windowURL': 'window_url',
}

PRODUCT_ID_TO_HOOK = {
    'spk_rating_long': 'hooks.zapier.com/hooks/catch/2517134/o3qhca0/',
    'rating_long': 'hooks.zapier.com/hooks/catch/2517134/o3qhca0/',
    'rating_short': 'hooks.zapier.com/hooks/catch/2517134/o3qhca0/',
    'sell': 'hooks.zapier.com/hooks/catch/2517134/o356ehs/',
    'tax': 'hooks.zapier.com/hooks/catch/2517134/odq2hzt/',
    'ratingv2': 'hooks.zapier.com/hooks/catch/2517134/owv1qgv/',
}


def current_ts():
    return datetime.now().isoformat()


def map_message_to_zapier(entity_name, message):
    mapped = {
        'intent': '',
        'intent_de': '',
    }

    for orig_k, v in message.items():
        if isinstance(v, str):
            # special handling for intent fields
            if orig_k == 'valution_intent' or orig_k == 'tax_intent':
                mapped['intent'] += v

            if orig_k == 'valution_intent_de' or orig_k == 'tax_intent_de':
                mapped['intent_de'] += v

        do_map = None
        for to_k, from_k in MAPPING.items():
            if from_k == orig_k:
                do_map = to_k
                break
        if do_map:
            mapped[to_k] = v
        else:
            mapped[orig_k] = v

    return mapped


def to_zapier_object(carl_id, hook_url, za_response):
    ret = {'carl_id': carl_id, 'hook_url': hook_url}
    ret['transferred_at'] = datetime.now().astimezone().isoformat()
    for k, v in za_response.items():
        ret['za_' + k] = v

    return {
        'key': str(uuid4()),
        'payload': ret,
        'version': 'v1',
    }


def product_id_to_hook_url(message):
    return PRODUCT_ID_TO_HOOK[message['payload']
                              ['product_id'].lower()].split('/', 1)


def save_zapier_execution(message):
    try:
        host, port = STORE_HOST.split(':', 1)
    except ValueError:
        host = STORE_HOST
        port = 443

    if port != 443:
        connection = http.client.HTTPConnection(host, port)
    else:
        connection = http.client.HTTPSConnection(host, port)

    connection.request('POST', STORE_PATH, message, {
                       'Content-Type': 'application/json', 'Authorization': f'Token {STORE_KEY}'})

    logging.info(f'zapier_start service: {connection.getresponse().read()}')
