import logging
from ldap3 import Server, Connection, TLS, get_config_parameter, set_config_parameter, SASL, ALL

from django.contrib.auth.models import User

from coldfront.core.utils.common import import_from_settings
from coldfront.core.allocation.models import Allocation, AllocationUser
from coldfront.core.project.models import Project, ProjectAttribute

from coldfront_plugin_auto_ldap.utils import connect

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

def get_project(allocation_pk):
    allocation = Allocation.objects.get(pk=allocation_pk)
    return allocation.project.title

def add_group(allocation_pk):
    conn = connect()
    uri = parse_uri(LDAP_SERVER_URI)
    project = get_project(allocation_pk)
    #search for group
    search_base = 'cn=' + project + uri # this probably needs fixing
    search_scope = 'base'
    search_filter = '(objectClass=*)'
    try:
        conn.search(search_base=search_base,
                    search_filter=search_filter,
                    search_scope=search_scope) # this probably needs fixing
        results = connection.entries
    except LDAPException as e:
        resutls = e
    
    # some kind of check here to see if the group was found
    if len(conn.entries) == 0:
        try:
            response = conn.add('cn=' + project + ",ou=coldfront" + uri, ['groupOfNames', 'top']) #this probably needs fixing
        except LDAPException as e:
            logger.warn(e)
    
    conn.unbind()

def add_user(allocation_user_pk):
    conn = connect()
    uri = parse_uri(LDAP_SERVER_URI)
    user = AllocationUser.objects.get(pk=allocation_user_pk)
    username = user.user.username
    user_first = user.user.first_name
    user_last = user.user.last_name
    project = user.allocation.project.title

    # check if user exists, create if they don't - maybe, might be able to just use existing users in ldap
    search_base = uri # this probably needs fixing
    search_scope = SUBTREE
    search_filter = '(uid=' + username + ')'
    try:
        conn.search(search_base=search_base,
                    search_filter=search_filter,
                    search_scope=search_scope)
        results = connection.entries
    except LDAPException as e:
        results = e

    if len(conn.entries) == 0:
        try:
            response = conn.add('uid=' + username + ",ou=coldfront", + uri, ['inetOrgPerson', 'top']) #this probably needs fixing
        except LDAPException as e:
            logger.warn(e)
            conn.unbind()
            return

    # add user to project's group
    search_base = 'cn=' + project + uri # this probably needs fixing
    search_scope = 'base'
    search_filter = '(objectClass=*)'
    try:
        conn.search(search_base=search_base,
                    search_filter=search_filter,
                    search_scope=search_scope) # this probably needs fixing
        results = connection.entries
    except LDAPException as e:
        resutls = e

    if len(conn.entries) != 0:
        conn.modify('cn=' + project + ",ou=coldfront" + uri, {'member': [(MODIFY_ADD, ['uid=' + username + ",ou=coldfront"])]}) #this probably needs fixing

    conn.unbind()

def remove_user(allocation_user_pk):
    conn = connect()
    uri = parse_uri(LDAP_SERVER_URI)
    user = AllocationUser.objects.get(pk=allocation_user_pk)
    username = user.user.username
    user_first = user.user.first_name
    user_last = user.user.last_name
    project = user.allocation.project.title

    # sheck if user exists
    search_base = uri # this probably needs fixing
    search_scope = SUBTREE
    search_filter = '(uid=' + username + ')'
    try:
        conn.search(search_base=search_base,
                    search_filter=search_filter,
                    search_scope=search_scope)
        results = connection.entries
    except LDAPException as e:
        results = e

    # remove if they do
    search_base = 'cn=' + project + uri # this probably needs fixing
    search_scope = 'base'
    search_filter = '(objectClass=*)'
    try:
        conn.search(search_base=search_base,
                    search_filter=search_filter,
                    search_scope=search_scope) # this probably needs fixing
        results = connection.entries
    except LDAPException as e:
        resutls = e

    if len(conn.entries) != 0:
        conn.modify('cn=' + project + ",ou=coldfront" + uri, {'member': [(MODIFY_DELETE, ['uid=' + username + ",ou=coldfront"])]}) #this probably needs fixing
        
    conn.unbind()
