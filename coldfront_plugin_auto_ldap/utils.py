import logging

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

def connect():
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
