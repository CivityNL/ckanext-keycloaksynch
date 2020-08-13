import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckanext.keycloaksynch.logic.action.update as action_update
import ckanext.keycloaksynch.logic.auth.update as auth_update


class KeycloaksynchPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IRoutes, inherit=True)


    """
    IAction
    """
    def get_actions(self):
        return {
            'users_keycloak_synch': action_update.users_keycloak_synch
        }


    """
    IAuthFunctions
    """
    def get_auth_functions(self):
        return {
            'users_keycloak_synch': auth_update.users_keycloak_synch
        }


    """
    IConfigurer
    """
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'keycloaksynch')

    """
    IRoutes
    """
    def before_map(self, map):
        map.connect('admin_keycloak', '/ckan-admin/keycloak',
                    controller='ckanext.keycloaksynch.controllers.keycloak:KeycloakController',
                    action='index')
        map.connect('admin_keycloak_synch', '/ckan-admin/keycloak_synch',
                    controller='ckanext.keycloaksynch.controllers.keycloak:KeycloakController',
                    action='synch')
        return map

