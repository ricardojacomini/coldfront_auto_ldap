from django.apps import AppConfig

class AutoLDAPConfig(AppConfig):
    name = "coldfront_plugin_auto_ldap"

    def ready(self):
        import coldfront_plugin_auto_ldap.signals
