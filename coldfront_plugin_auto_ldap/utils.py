import logging
from ldap3 import Server, Connection, TLS, get_config_parameter, set_config_parameter, SASL, ALL

from coldfront.core.utils.common import import_from_settings

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

def parse_uri(uri):
    if "://" in uri:
        uri = uri.split("/")[2]
    else:
        uri = uri.split("/")[0]
    partURI = uri.split(".")
    parsed = ""
    for part in partURI:
        parsed += ',dc=' + part
    return parsed

URI = parse_uri(LDAP_SERVER_URI)

def connect(uri = URI):
    tls = None
    if LDAP_USE_TLS:
        tls = Tls(
            local_private_key_file=LDAP_PRIV_KEY_FILE,
            local_certificate_file=LDAP_CERT_FILE,
            ca_certs_file=LDAP_CACERT_FILE,
        )
    server = Server(LDAP_SERVER_URI, use_ssl=LDAP_USE_SSL, connect_timeout=LDAP_CONNECT_TIMEOUT, tls=tls)
    conn_params = {"auto_bind": True}
    if LDAP_SASL_MECHANISM:
        conn_params["sasl_mechanism"] = LDAP_SASL_MECHANISM
        conn_params["sasl_credentials"] = LDAP_SASL_CREDENTIALS
        conn_params["authentication"] = SASL
    conn = Connection(server, LDAP_BIND_DN, LDAP_BIND_PASSWORD, **conn_params)
    return conn

def search_project(conn, project, uri = URI):
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

def add_project(conn, project, uri = URI):
    try:
        response = conn.add('cn=' + project + ",ou=coldfront" + uri, ['groupOfNames', 'top']) #this probably needs fixing
    except LDAPException as e:
        logger.warn(e)

def search_user(conn, username, uri = URI):
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

def add_user(conn, username, uri = URI):
    try:
        response = conn.add('uid=' + username + ",ou=coldfront", + uri, ['inetOrgPerson', 'top']) #this probably needs fixing
    except LDAPException as e:
        logger.warn(e)

def add_user_group(conn, username, group, uri = URI):
    search_project(conn, project, uri)

    if len(conn.entries) != 0:
        try:
            conn.modify('cn=' + project + ",ou=coldfront" + uri, {'member': [(MODIFY_ADD, ['uid=' + username + ",ou=coldfront"])]}) #this probably needs fixing
        except LDAPException as e:
            results = e
            return -1

def remove_user_group(conn, username, uri = URI):
    search_project(conn, project, uri)

    if len(conn.entries) != 0:
        try:
            conn.modify('cn=' + project + ",ou=coldfront" + uri, {'member': [(MODIFY_DELETE, ['uid=' + username + ",ou=coldfront"])]}) #this probably needs fixing
        except LDAPException as e:
            results = e
            return -1
