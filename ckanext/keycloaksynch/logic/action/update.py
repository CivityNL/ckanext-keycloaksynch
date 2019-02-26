# -*- coding: utf-8 -*-
from ckan.plugins import toolkit
import base64
import json
import requests
import threading
import logging

log = logging.getLogger(__name__)


@toolkit.side_effect_free
def keycloak_synch(context, data_dict):
    context['ignore_auth'] = True

    # log.info('Preparing the Thread')
    # thread = threading.Thread(target=_keycloak_synch, args=(context.copy(), data_dict))
    # log.info('Thread setup')
    # thread.daemon = True  # Daemonize thread
    # log.info('Thread Demonized')
    # thread.start()  # Start the execution
    # log.info('Exiting Action Call')


    log.info('keycloak_synch Called')
    _keycloak_synch(context.copy(), data_dict)
    log.info('Finished keycloak_synch ')


    return {'success': True}


def _keycloak_synch(context, data_dict):
    log.info('Thread Started Exectuion')

    log.info('Requesting Access Token')
    access_token = _get_admin_kc_access_token()
    log.info('Getting total count of Keycloak Users')
    user_count = _get_total_count_kc_users(access_token)
    log.info('Getting Keycloak User List')
    kc_user_list = _get_kc_user_list(access_token, user_count)
    log.info('Updating CKAN based on Keycloak')
    keycloack_username_list = _update_ckan_users_based_on_kc_user_list(context.copy(), kc_user_list)
    log.info('Deleting CKAN Users that are not in Keycloak')
    _delete_ckan_users_not_in_kc_user_list(context.copy(), keycloack_username_list)
    log.info('Thread Finished Exectuion')


def _get_admin_kc_access_token():
    log.info('Get Values from Config File')
    # Get Values from Config File
    token_endpoint = toolkit.config.get("ckan.oauth2.admin_token_endpoint")
    log.info('token_endpoint = {0}'.format(token_endpoint))
    admin_client_id = toolkit.config.get("ckan.oauth2.admin_client_id")
    log.info('admin_client_id = {0}'.format(admin_client_id))
    admin_client_secret = toolkit.config.get("ckan.oauth2.admin_client_secret")
    log.info('admin_client_secret = {0}'.format(admin_client_secret))

    encoded_auth = base64.b64encode('{0}:{1}'.format(admin_client_id,
                                                     admin_client_secret))

    # GET authentication token to access Admin REST API
    url = token_endpoint
    payload = "grant_type=client_credentials"
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Authorization': "Basic {0}".format(encoded_auth)
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    response_dict = json.loads(response.text)
    log.info('response_dict = {0}'.format(response_dict))
    access_token = response_dict['access_token']
    log.info('access_token = {0}'.format(access_token))

    return access_token


def _get_total_count_kc_users(access_token):
    # GET the total count of Users
    payload = "grant_type=client_credentials"
    url = "https://acc-datadenhaag.dataplatform.nl/auth/admin/realms/Data-Catalog/users/count"
    headers = {
        'Authorization': "Bearer {0}".format(access_token)
    }
    response = requests.request("GET", url, data=payload, headers=headers)
    user_count = json.loads(response.text)
    return user_count


def _get_kc_user_list(access_token, user_count):
    # GET the list of users from Keycloak
    url = "https://acc-datadenhaag.dataplatform.nl/auth/admin/realms/Data-Catalog/users"
    querystring = {"max": str(user_count)}
    payload = ""
    headers = {
        'Authorization': "Bearer {0}".format(access_token)
    }
    response = requests.request("GET", url, data=payload, headers=headers,
                                params=querystring)
    kc_user_list = json.loads(response.text)
    return _kc_usr_list_reformat(kc_user_list)


def _kc_usr_list_reformat(kc_user_list):
    # print 'Reformat Users form Keycloak'
    i = 0
    clean_user_list = list()
    for kc_user in kc_user_list:
        # print '{0}: Reofrmating Keycloak User {1}'.format(i, kc_user['username'])
        # Get all Info from each User
        name = kc_user['username']
        if kc_user['enabled']:
            state = 'active'
        else:
            state = 'deleted'

        email = kc_user['email']
        fullname = kc_user['firstName'] + ' ' + kc_user['lastName']

        clean_kc_user_dict = {
            'name': name,
            'state': state,
            'email': email,
            'fullname': fullname,
            'password': 'password'
        }

        clean_user_list.append(clean_kc_user_dict)
        i = i + 1
        # if i == 1:
        #     break

    return clean_user_list


def _update_ckan_users_based_on_kc_user_list(context, kc_user_list):
    # print 'Make changes on CKAN based on Keycloak User list'
    keycloack_username_list = list()
    for kc_user in kc_user_list:
        # print 'Synchronizing Keycloak user "{0}" in CKAN'.format(kc_user['name'])
        keycloack_username_list.append(kc_user['name'])

        try:
            user_dict = toolkit.get_action('user_show')(context.copy(), {'id': kc_user['name']})
            # The user exists
            # print 'user was found on CKAN'

            if kc_user['state'] == 'deleted':
                # print 'User is Disabled on Keycloak and therefore the CKAN user is going to be DELETED'
                toolkit.get_action('user_delete')(context.copy(), {'id': kc_user['name']})
                continue

            # print 'CKAN user information is going to be updated'

            for key, value in kc_user.items():
                user_dict[key] = value

            # CKAN user_update Call
            toolkit.get_action('user_update')(context.copy(), user_dict)

        except toolkit.ObjectNotFound:
            ## ADD USER
            # print 'User was not found in CKAN, Adding it now.'
            toolkit.get_action('user_create')(context.copy(), kc_user)
    return keycloack_username_list



def _delete_ckan_users_not_in_kc_user_list(context, keycloack_username_list):


    # print 'Getting all CKAN Users and Delete all that are not present in Keycloak'
    # print 'keycloack_username_list = {0}'.format(keycloack_username_list)
    ckan_user_list = toolkit.get_action('user_list')(context.copy(), {})

    i = 0
    for ckan_user in ckan_user_list:
        # print '{0}: Checking CKAN user "{1}" in keycloak'.format(i, ckan_user['name'])
        if ckan_user['name'] == 'admingil':
            continue


        if ckan_user['name'] not in keycloack_username_list:
            # print 'User not found in Keycloak, is going to be deleted'
            try:
                toolkit.get_action('user_delete')(context.copy(), {'id': ckan_user['name']})
            except toolkit.NotAuthorized:
                log.info('Not Authorized to delete user "{0}"'.format(ckan_user['name']))
        i = i + 1
