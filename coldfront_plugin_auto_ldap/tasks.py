import logging
from ldap3 import Server, Connection, TLS, get_config_parameter, set_config_parameter, SASL

from coldfront.core.utils.common import import_from_settings
from coldfront.core.allocation.models import Allocation, AllocationUser

logger = logging.getLogger(__name__)

def add_group(allocation_pk):
    pass

def add_user(allocation_user_pk):
    pass

def remove_user(allocation_user_pk):
    pass
