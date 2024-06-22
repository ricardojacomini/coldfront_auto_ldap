# coldfront_auto_ldap
A [ColdFront](https://coldfront.readthedocs.io/en/latest/) plugin that automatically creates ldap an ldap group when a project is approved and manages users in the group
## Installation
If you're using a virtual environment (following ColdFront's deployment instructions should have you make and use a virtual environment), make sure you're in the virutal environment first.
```
pip install git+https://github.com/ricardojacomini/coldfront_auto_ldap.git
```
## Configuration
Add the following to ColdFront's [local settings](https://coldfront.readthedocs.io/en/latest/config/#configuration-files):
```
INSTALLED_APPS += ["coldfront_plugin_auto_ldap"]
AUTO_LDAP_COLDFRONT_OU = Coldfront OU
```
The Coldfront OU is the LDAP OU this plugin will use. If not set, it will default to "COLDFRONT"
