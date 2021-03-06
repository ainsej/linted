from django.core.management.base import BaseCommand
from django.conf import settings
from scanners.install import install_scanner


class Command(BaseCommand):
    help = 'Builds dockerfiles for ENABLED_SCANNERS'
    option_list = BaseCommand.option_list

    def handle(self, *args, **options):
        for scanner_name in settings.ENABLED_SCANNERS:
            install_scanner(scanner_name)
