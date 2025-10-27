from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):

    def handle(self, *args, **options):
        Group.objects.all().delete()
        Permission.objects.all().delete()

        call_command("loaddata", "groups_and_permissions.json")

        self.stdout.write(
            self.style.SUCCESS("Successfully loaded groups and permissions")
        )
