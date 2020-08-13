# ckanext-keycloaksynch


CKAN extensions used to Synchronize users from a Keycloak Realm to CKAN DB.

## Features

- Creates/Updates all users from Keycloak into CKAN DB.

- Deletes users from CKAN that fit the following requirements:
    - Not present in Keycloak.
    - Present in Keycloak but not enabled.

- It's possible to protect some users in CKANfrom being deleted by setting up the config option ``ckanext.keycloaksynch.protected_users``. See bellow [Config Settings](#Config Settings).

## Requirements

- CKAN (tested on 2.8.2 version)
- Keycloak Instance (tested with 8.0 version)


## Setting Up Keycloak

It's expected minimum familiarity with Keycloak but if needed here is the [Keycloak Documentation](https://www.keycloak.org/documentation.html)

    Note: You must be logged in as an Keycloak Admin to following the next steps.

1 - Create/Use your desired Realm, and populate it with users.

2 - Setup the ``admin-cli`` Client of the **Master Realm**.

  - Select the *Master Realm* -> *Clients* -> *admin-cli*
  - In the *Settings* Tab make sure the following values are set correctly and press **Save**:
    - Enabled: ON
    - Client Protocol: openid-connect
    - Access Type: confidential
    - Service Accounts Enabled: ON

3 - Obtain the Client Secret to provide in the  ``ckanext.keycloaksynch.admin_client_secret`` config setting.
  - Select the *Master Realm* -> *Clients* -> *admin-cli*
  - The *Credentials* tab is where the Secret can be found. (if you can't find the tab, make sure Step 2 was done correctly)

4 - Setup Permissions for user management in the desired Realm.
  - Select the *Desired Realm* -> *Clients* -> *admin-cli*
  - Go to the *Service Account Roles* tab.
  - Select your Desired Realm from the *Client Roles* selection box.
  - Assign ***view-users*** and ***manage-users*** roles from the *Available Roles* list. 
  

## Installation

Once you have your Keycloak setup correctly it's time to install the extension:

1. Activate your CKAN virtual environment, for example:
    ```
    . /usr/lib/ckan/default/bin/activate
    ```
2. Clone and Install the ckanext-keycloaksynch Python package into your virtual environment:
    ```
    git clone https://github.com//ckanext-keycloaksynch.git
    cd ckanext-keycloaksynch
    python setup.py develop
    pip install -r dev-requirements.txt
    ```

3. Add ``keycloaksynch`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``):

    ```
    ckan.plugins = keycloaksynch ...
    ```

4. Restart CKAN. For example if you've deployed CKAN with HTTPD:

    ```
    systemctl restart httpd
    ```


## Config Settings

Following configuration options should be set in your CKAN config file:

    # Client ID for admin access
    ckanext.keycloaksynch.admin_client_id = admin-cli
    
    # Client Secret for admin access
    ckanext.keycloaksynch.admin_client_secret = ***************
    
    # Token Endpoint for admin access
    ckanext.keycloaksynch.admin_token_endpoint = https://tst-login.dataplatform.nl/auth/realms/master/protocol/openid-connect/token
    
    # Default Password assigned to newly created user in the CKAN DB (not in Keycloak)
    ckanext.keycloaksynch.default_password = *******
    
    # List (space separated) of ckan users should not be deleted
    # in case they are not present or disabled in Keycloak
    ckanext.keycloaksynch.protected_users = arjen bas ber erik frits georgios gil isabela jurgen mathieu michael stephanie
    
    # Keycloak endpoint to query Users
    ckanext.keycloaksynch.users_endpoint = https://tst-login.dataplatform.nl/auth/admin/realms/Data-Catalog/users
    
    # Keycloak enpoint to query User Count
    ckanext.keycloaksynch.users_count_endpoint = https://tst-login.dataplatform.nl/auth/admin/realms/Data-Catalog/users/count

