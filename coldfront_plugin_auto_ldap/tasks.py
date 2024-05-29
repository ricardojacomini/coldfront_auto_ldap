import logging
from ldap3 import Server, Connection, TLS, get_config_parameter, set_config_parameter, SASL, ALL

from django.contrib.auth.models import User

from coldfront.core.utils.common import import_from_settings
from coldfront.core.allocation.models import Allocation, AllocationUser
from coldfront.core.project.models import Project, ProjectAttribute

from coldfront_plugin_auto_ldap.utils import (
    connect,
    parse_uri,
    search_project,
    add_project,
    search_user,
    add_user,
    add_user_group,
    remove_user_group
)

logger = logging.getLogger(__name__)

LDAP_SERVER_URI = import_from_settings("LDAP_USER_SEARCH_SERVER_URI")
LDAP_USER_SEARCH_BASE = import_from_settings("LDAP_USER_SEARCH_BASE")
LDAP_BIND_DN = import_from_settings("LDAP_USER_SEARCH_BIND_DN", None)
LDAP_BIND_PASSWORD = import_from_settings("LDAP_USER_SEARCH_BIND_PASSWORD", None)
LDAP_CONNECT_TIMEOUT = import_from_settings("LDAP_USER_SEARCH_CONNECT_TIMEOUT", 2.5)
LDAP_USE_SSL = import_from_settings("LDAP_USER_SEARCH_USE_SSL", True)
LDAP_USE_TLS = import_from_settings("LDAP_USER_SEARCH_USE_TLS", False)
LDAP_SASL_MECHANISM = import_from_settings("LDAP_USER_SEARCH_SASL_MECHANISM", None)
LDAP_SASL_CREDENTIALS = import_from_settings("LDAP_USER_SEARCH_SASL_CREDENTIALS", None)
LDAP_PRIV_KEY_FILE = import_from_settings("LDAP_USER_SEARCH_PRIV_KEY_FILE", None)
LDAP_CERT_FILE = import_from_settings("LDAP_USER_SEARCH_CERT_FILE", None)
LDAP_CACERT_FILE = import_from_settings("LDAP_USER_SEARCH_CACERT_FILE", None)

ou = import_from_settings("AUTO_LDAP_COLDFRONT_OU")

# gets the project title from an allocation_pk
def get_project(allocation_pk):
    allocation = Allocation.objects.get(pk=allocation_pk)
    return allocation.project.title

# creates a new project
def add_group(allocation_pk):
    conn = connect()
    project = get_project(allocation_pk)
    #search for group
    search_project(conn, project)
    
    # some kind of check here to see if the group was found
    add_project(conn, project)
    
    conn.unbind()

# creates user if it doesn't already exist and adds them to a project
def add_user(allocation_user_pk):
    conn = connect()
    user = AllocationUser.objects.get(pk=allocation_user_pk)
    username = user.user.username
    user_first = user.user.first_name
    user_last = user.user.last_name
    project = user.allocation.project.title

    # check if user exists, create if they don't - maybe, might be able to just use existing users in ldap
    search_user(conn, username)

    if len(conn.entries) == 0:
        add_user(conn, username)

    # add user to project's group
    add_user_group(conn, usernmae, project)

    conn.unbind()

# removes a user from a project
def remove_user(allocation_user_pk):
    conn = connect()
    user = AllocationUser.objects.get(pk=allocation_user_pk)
    username = user.user.username
    user_first = user.user.first_name
    user_last = user.user.last_name
    project = user.allocation.project.title

    # sheck if user exists
    search_user(conn, username)

    if len(conn.entries) == 0:
        conn.unbind()
        return

    # remove if they do
    remove_user_group(conn, username, project)
        
    conn.unbind()
