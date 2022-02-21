# -*- coding: utf-8 -*-
import logging

log = logging.getLogger(__name__)


def deleted_user_list(context, data_dict):
    # Only Sysadmins or Context ignore_auth=true
    if context.get('ignore_auth'):
        return {'success': True}
    return {'success': False}

