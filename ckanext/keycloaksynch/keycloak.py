# -*- coding: utf-8 -*-
import logging
import base64
import requests
import json
import ckan.plugins.toolkit as tk
import constants as const

log = logging.getLogger(__name__)


def get_access_token():

    admin_client_id = tk.config.get(const.ADMIN_CLIENT_ID_CONFIG)
    admin_client_secret = tk.config.get(const.ADMIN_CLIENT_SECRET_CONFIG)
    encoded_auth = base64.b64encode('{0}:{1}'.format(admin_client_id, admin_client_secret))

    url = tk.config.get(const.ADMIN_TOKEN_ENDPOINT_CONFIG)
    payload = "grant_type=client_credentials"
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Authorization': "Basic {0}".format(encoded_auth)
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    # TODO Error Handling
    access_token = json.loads(response.text)['access_token']

    return access_token


def get_users_count():

    access_token = get_access_token()

    url = tk.config.get(const.USERS_COUNT_ENDPOINT)
    payload = "grant_type=client_credentials"
    headers = {'Authorization': "Bearer {0}".format(access_token)}

    response = requests.request("GET", url, data=payload, headers=headers)
    # TODO Error Handling
    user_count = json.loads(response.text)

    return user_count


def get_users():

    access_token = get_access_token()
    user_count = get_users_count()

    params = {"max": str(user_count)}
    url = tk.config.get(const.USERS_ENDPOINT)
    headers = {'Authorization': "Bearer {0}".format(access_token)}

    response = requests.request("GET", url, headers=headers, params=params)
    # TODO Error Handling
    kc_users = json.loads(response.text)

    return kc_users

