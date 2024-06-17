import logging

from django.core.management.base import BaseCommand, CommandError

from coldfront.core.project.models import Project, ProjectAttribute, ProjectUser
from coldfront.core.user.models import User, UserAtrribute

from coldfront_plugin_auto_ldap.utils import (
    connect,
    disconnect,
    parse_uri,
    search_project,
    add_project,
    search_user,
    search_user_group,
    add_user,
    add_user_group,
    remove_user_group
)

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help="Search for a user or group in LDAP"

    def add_arguments(self, parser):
        parser.add_argument(
            "-u",
            "--user",
            help="Specify the user to search for. Use -p to specify the project to search in"
        )
        parser.add_argument(
            "-p",
            "--project",
            help="Specify the project to search for. Use -u to search for a user in the project"
        )

    def handle(self, *args, **options):
        user = options["user"]
        project = options["project"]

        if user == None and project == None:
            logger.warn("Usage error: no arguments given")
            return

        conn = connect()

        if user != None:
            if project != None:
                search_user_group(conn, user, project)
            else:
                search_user(conn, user)
        else:
            search_project(conn, project)

        disconnect(conn)
