# -*- coding: utf-8 -*-
import ckan.plugins.toolkit as tk
import logging
import ckanext.keycloaksynch.jobs as jobs

log = logging.getLogger(__name__)


@tk.side_effect_free
def users_keycloak_synch(context, data_dict):
    
    tk.check_access('users_keycloak_synch', context, data_dict)

    tk.enqueue_job(jobs.users_keycloak_synch)

    return {'success': True}

