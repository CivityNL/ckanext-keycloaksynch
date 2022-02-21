# -*- coding: utf-8 -*-
import ckan.plugins.toolkit as tk
import logging

log = logging.getLogger(__name__)


@tk.side_effect_free
def deleted_user_list(context, data_dict):
    '''Return a list of the site's deketed user accounts.
    '''
    model = context['model']
    tk.check_access('deleted_user_list', context, data_dict)

    query = model.Session.query(model.User.name)
    # Filter for deleted users
    query = query.filter(model.User.state == model.State.DELETED)
    users_list = []
    for user in query.all():
        users_list.append(user[0])

    return users_list
