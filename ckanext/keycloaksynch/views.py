from flask.views import MethodView
from flask import Blueprint

import ckan.model as model
import ckan.plugins.toolkit as toolkit
import logging

log = logging.getLogger(__name__)


class KeycloakSynchView(MethodView):

    def get(self):
        log.info('KeycloakSynchView::get')
        return toolkit.render(u'admin/keycloak.html')

    def post(self):
        log.info('KeycloakSynchView::post')
        context = {'model': model, 'session': model.Session,
                   'user': toolkit.g.user, 'auth_user_obj': toolkit.g.userobj}
        toolkit.get_action('users_keycloak_synch')(context, {})
        toolkit.h.flash_success('Synchronization Triggered.')
        return toolkit.redirect_to('keycloaksynch.keycloak')


def get_blueprint():
    blueprint = Blueprint('keycloaksynch', __name__)
    blueprint.add_url_rule(u'/ckan-admin/keycloak_synch', view_func=KeycloakSynchView.as_view(str(u'keycloak')))
    return blueprint
