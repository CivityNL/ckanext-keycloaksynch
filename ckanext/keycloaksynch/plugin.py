import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckanext.keycloaksynch.logic.action.update as action_update


class KeycloaksynchPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.IActions)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'keycloaksynch')


    """
    IRoutes
    """

    def before_map(self, map):
        # Workflow Triggers
        map.connect('admin_keycloak', '/ckan-admin/keycloak',
                    controller='ckanext.keycloaksynch.controllers.keycloak:KeycloakController',
                    action='index')
        map.connect('admin_keycloak_synch', '/ckan-admin/keycloak_synch',
                    controller='ckanext.keycloaksynch.controllers.keycloak:KeycloakController',
                    action='synch')
        return map

    """
    IAction
    """

    def get_actions(self):
        return {
            'keycloak_synch': action_update.keycloak_synch
        }
