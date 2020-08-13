# ------------------------
# CONFIGURATION OPTIONS
# ------------------------

ADMIN_CLIENT_ID_CONFIG = "ckanext.keycloaksynch.admin_client_id"
ADMIN_CLIENT_SECRET_CONFIG = "ckanext.keycloaksynch.admin_client_secret"
ADMIN_TOKEN_ENDPOINT_CONFIG = "ckanext.keycloaksynch.admin_token_endpoint"

# Password for the newly created users (only used if keycloaksynch is disabled)
DEFAULT_PASSWORD = "ckanext.keycloaksynch.default_password"

# Users to not eliminate
PROTECTED_USERS = "ckanext.keycloaksynch.protected_users"

# "https://catalogusdenhaag.dataplatform.nl/auth/admin/realms/Data-Catalog/users"
USERS_ENDPOINT = "ckanext.keycloaksynch.users_endpoint"

# "https://catalogusdenhaag.dataplatform.nl/auth/admin/realms/Data-Catalog/users/count"
USERS_COUNT_ENDPOINT = "ckanext.keycloaksynch.users_count_endpoint"

