import logging

from django.core.management.base import BaseCommand, CommandError

from coldfront.core.project.models import Project, ProjectAttribute
from coldfront.core.user.models import User, UserAtrribute

from coldfront_plugin_auto_ldap.tasks import add_group, add_user

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Adds users or projects to LDAP"

    def add_arguments(self, parser):
        parser.add_argument(
            "-u",
            "--user",
            help="Add a user, use -p to specify a project to add the user to"
        )
        parser.add_argument(
            "-p",
            "--project",
            help="Add a project, or specify project when used with -u"
        )
        parser.add_argument(
            "-r",
            "--remove",
            action="store_true",
            help="Use with -r and -p to remove a user from a project"
        )

    def handle(self, *args, **options):
        projects = Allocation.objects.all()
        users = User.objects.all()

        user = options["user"]
        project = options["project"]

        if user != None:
            if project != None:
                if options["remove"]:
                    pass
                else:
                    pass
            pass
        elif project:
            pass
        else:
            for p in projects:
                pass
            for u in users:
                pass
