# -*- coding: utf-8 -*-
import logging
import base64
import sys

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


def get_users(query=None):
    access_token = get_access_token()
    user_count = get_users_count()

    params = {"max": str(user_count)}
    if query:
        params['username'] = query
    url = tk.config.get(const.USERS_ENDPOINT)
    headers = {'Authorization': "Bearer {0}".format(access_token)}

    response = requests.request("GET", url, headers=headers, params=params)
    kc_users = json.loads(response.text)

    return kc_users


def get_user_id(username):
    lower_user_name = username.lower()
    users = get_users(query={"username": lower_user_name})
    return next((user["id"] for user in users if user["username"] == lower_user_name), None)


def user_create(user_dict):
    log.info('Keycloak user_create: {}'.format(user_dict['username']))
    access_token = get_access_token()

    url = tk.config.get(const.USERS_ENDPOINT)
    headers = {'Content-Type': "application/json",
               'Authorization': "Bearer {0}".format(access_token)}
    data = json.dumps(user_dict)
    response = requests.request("POST", url, headers=headers, data=data)
    log.info('Response ({}) :  {}'.format(response.status_code, response.text))

    return response


def user_update(user_dict):
    log.info('Keycloak user_create: {}'.format(user_dict['username']))
    access_token = get_access_token()

    url = '{}/{}'.format(tk.config.get(const.USERS_ENDPOINT), user_dict['id'])
    headers = {'Content-Type': "application/json",
               'Authorization': "Bearer {0}".format(access_token)}
    data = json.dumps(user_dict)
    response = requests.request("PUT", url, headers=headers, data=data)
    log.info('Response ({}) :  {}'.format(response.status_code, response.text))

    return response


def user_upsert(user_dict):
    username = user_dict['username']
    user_kc_id = get_user_id(username)

    if user_kc_id:
        user_dict['id'] = user_kc_id
        user_update(user_dict)
    else:
        user_create(user_dict)
