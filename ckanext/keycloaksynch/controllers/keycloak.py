import ckan.model as model
import ckan.plugins.toolkit as toolkit
import logging
from ckan.lib import base

log = logging.getLogger(__name__)


class KeycloakController(base.BaseController):


    def index(self):
        return base.render(u'admin/keycloak.html')


    def synch(self):
        context = {'model': model, 'session': model.Session,
                   'user': toolkit.c.user, 'auth_user_obj': toolkit.c.userobj}

        log.info('Calling Action')
        toolkit.get_action('keycloak_synch')(context, {})
        log.info('Rendering the page again')
        toolkit.h.flash_success('Synchronization Finished Sucessfully.')

        return toolkit.redirect_to('admin_keycloak')
