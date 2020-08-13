# -*- coding: utf-8 -*-
import logging

log = logging.getLogger(__name__)


def users_keycloak_synch(context, data_dict):
    # Only Sysadmins
    return {'success': False}

