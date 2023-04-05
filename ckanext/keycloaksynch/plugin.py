import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckanext.keycloaksynch.logic.action.get as action_get
import ckanext.keycloaksynch.logic.action.update as action_update
import ckanext.keycloaksynch.logic.auth.get as auth_get
import ckanext.keycloaksynch.logic.auth.update as auth_update
import ckanext.keycloaksynch.views as views


class KeycloaksynchPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)

    """
    IAction
    """

    def get_actions(self):
        return {
            'users_keycloak_synch': action_update.users_keycloak_synch,
            'deleted_user_list': action_get.deleted_user_list
        }

    """
    IAuthFunctions
    """

    def get_auth_functions(self):
        return {
            'users_keycloak_synch': auth_update.users_keycloak_synch,
            'deleted_user_list': auth_get.deleted_user_list
        }

    """
    IConfigurer
    """
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')


    # IBlueprint
    def get_blueprint(self):
        u'''Return a Flask Blueprint object to be registered by the app.'''
        return views.get_blueprint()
