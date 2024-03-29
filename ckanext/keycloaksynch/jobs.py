# -*- coding: utf-8 -*-
import logging
import ckan.model as model
import ckan.plugins.toolkit as tk
import keycloak as kc
import constants as const

log = logging.getLogger(__name__)


def users_keycloak_synch():
    context = {'model': model, 'session': model.Session, 'ignore_auth': True, 'user': None}

    kc_users = kc.get_users()

    upsert_users_from_keycloak(context, kc_users)

    delete_ckan_users_from_keycloak(context, kc_users)

    populate_keycloak_with_deleted_ckan_users(context)


def upsert_users_from_keycloak(context, kc_users):
    log.info('Upserting Users from Keycloak')
    for kc_user in kc_users:
        log.info('Handling Keycloak User: {}'.format(kc_user['username']))
        if not kc_user['enabled']:
            continue
        if not kc_user['username']:
            continue
        if not kc_user['email']:
            continue
        if user_exists_in_ckan(context, kc_user['username']):
            update_user(context.copy(), kc_user)
        else:
            create_user(context.copy(), kc_user)


def delete_ckan_users_from_keycloak(context, kc_users):
    log.info('Deleting Users from CKAN')
    context['ignore_auth'] = True

    protected_users = tk.config.get(const.PROTECTED_USERS, '').split()
    ckan_users = tk.get_action('user_list')(context, {})

    for ckan_user in ckan_users:
        log.info('Handling CKAN User: {}'.format(ckan_user['name']))

        if ckan_user['name'] in protected_users:
            log.info('User in Protected list')
            continue

        user_exists_and_is_enabled_in_keycloak = any(
            kc_user['username'] == ckan_user['name'] and kc_user['enabled'] for
            kc_user in kc_users)
        if user_exists_and_is_enabled_in_keycloak:
            continue

        log.info('Deleting User')
        tk.get_action('user_delete')(context.copy(), {'id': ckan_user['name']})


def user_exists_in_ckan(context, user_name_or_id):
    try:
        tk.get_validator('user_id_or_name_exists')(user_name_or_id, context)
        return True
    except tk.Invalid:
        return False


def update_user(context, kc_user):
    log.info('Updating User')
    context['ignore_auth'] = True

    user_dict = tk.get_action('user_show')(context, {'id': kc_user['username']})

    user_dict['email'] = kc_user.get('email', '')
    user_dict['fullname'] = kc_user.get('firstName', '') + ' ' + kc_user.get('lastName', '')
    user_dict['state'] = 'active'
    try:
        tk.get_action('user_update')(context, user_dict)
    except tk.ValidationError as ex:
        pass


def create_user(context, kc_user):
    log.info('Creating User')

    fullname = kc_user.get('firstName', '') + ' ' + kc_user.get('lastName', '')

    user_dict = {
        'name': kc_user.get('username', ''),
        'email': kc_user.get('email', ''),
        'fullname': fullname,
        'password': tk.config.get(const.DEFAULT_PASSWORD, 'password')
    }

    tk.get_action('user_create')(context, user_dict)


def _convert_ckan_user_to_kc_user(ckan_user_dict):
    kc_user_dict = {
        "firstName": ckan_user_dict['fullname'],
        "email": ckan_user_dict['email'],
        "emailVerified": True,
        "enabled": False,
        "username": ckan_user_dict['name']
    }
    return kc_user_dict


def populate_keycloak_with_deleted_ckan_users(context):
    log.info('populate_keycloak_with_deleted_ckan_users')
    context['ignore_auth'] = True

    deleted_ckan_users = tk.get_action('deleted_user_list')(context, {})

    for username in deleted_ckan_users:
        log.info('Creating deleted user {} in Keycloak'.format(username))
        user_dict = tk.get_action('user_show')(context, {'id': username})
        kc_user_dict = _convert_ckan_user_to_kc_user(user_dict)
        kc.user_upsert(kc_user_dict)
